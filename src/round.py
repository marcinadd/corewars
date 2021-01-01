import copy
from random import randrange, sample

from src.core import Core
from src.enum.event import CoreEvent


class Round:
    def __init__(self, warriors, core=None, core_size=8000, init_warriors=True, gui=None, number=0, max_cycles=80000):
        """
        Round constructor
        :param warriors: Required warriors list
        :param core: Optional core for testing purposes
        :param core_size: Other core size than default
        :param init_warriors: Execute init_warriors() for testing purposes
        """
        self._core = core if core else Core(core_size, gui=gui)
        self._warriors = warriors
        if gui:
            self._gui = gui
            self._gui.init_game_screen()
        if init_warriors:
            self.init_warriors()
        self._number = number
        self._cycles = 0
        self._max_cycles = max_cycles

    def core(self):
        return self._core

    def warriors(self):
        return self._warriors

    def cycles(self):
        return self._cycles

    def _init_warrior(self, warrior, starting_core_address):
        """
        Loads warrior into core
        :param warrior: Warrior to be loaded
        :param starting_core_address: Core address where first instruction will be loaded
        """
        self._core[starting_core_address] = copy.copy(warrior.instructions())
        for offset, instruction in enumerate(warrior.instructions()):
            address = starting_core_address + offset
            self._core[address] = copy.copy(instruction)
            self._core.update_core_gui(address, warrior, CoreEvent.EXECUTE)
        warrior.add_process(starting_core_address)

    def init_warriors(self):
        """
        Iterates all warriors and loads them into core
        """
        core_size = self._core.size()
        start_position = randrange(core_size)
        space_between_warriors = core_size // len(self._warriors)

        shuffled_warriors = sample(self._warriors, len(self._warriors))
        for i, warrior in enumerate(shuffled_warriors):
            self._init_warrior(warrior, start_position + i * space_between_warriors)

    def is_ended(self):
        # TODO Support testing warriors with only one warrior in core
        return len(self.get_alive_warriors()) <= 1 or self._cycles > self._max_cycles

    def get_alive_warriors(self):
        """
        Return list of warriors which have at least one process
        :return: Alive warrior count
        """
        return [warrior for warrior in self._warriors if warrior.processes()]

    def update_warriors_results(self):
        """
        Update alive warrior results after round ended
        """
        alive_warriors = self.get_alive_warriors()
        if len(alive_warriors) == 1:
            # Only one alive warrior remained; increment its wins
            warrior = alive_warriors[0]
            warrior.warrior_info().inc_wins()
        else:
            # Round ended after reaching max_cycles; increment ties for any alive warrior
            for warrior in alive_warriors:
                info = warrior.warrior_info()
                info.inc_ties()

    def simulation_step(self):
        """
        Iterates all warriors and execute one queued instruction for each warrior
        """
        for warrior in self._warriors:
            if warrior.processes():
                instruction_pos = warrior.processes().pop(0)
                instruction = self._core[instruction_pos]
                instruction.execute(self._core, instruction_pos, warrior)
                self._cycles += 1
                if len(warrior.processes()) == 0:
                    # If warrior doesn't have processes it lost in this round
                    warrior.warrior_info().inc_loses()

    def play(self):
        """
        Executes simulation step and updates gui until round is not ended
        """
        self._gui.print_round_text(self._number)
        # Play game
        while not self.is_ended():
            self.simulation_step()
            self._gui.clock_tick()
            self._gui.print_game_info(self._warriors, self._cycles)
        # Update results
        self.update_warriors_results()
