import copy
from random import randrange

from src.core import Core
from src.enum.event import CoreEvent
from src.gui.colors import Color


class Game:
    def __init__(self, warriors, core=None, core_size=200, init_warriors=True, gui=None):
        """
        Game constructor
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
            self.set_warriors_colors()

    def core(self):
        return self._core

    def warriors(self):
        return self._warriors

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

        for i, warrior in enumerate(self._warriors):
            self._init_warrior(warrior, start_position + i * space_between_warriors)

    def set_warriors_colors(self):
        """
        Sets warrior colors from Color.WARRIOR_COLORS
        """
        for i, warrior in enumerate(self._warriors):
            warrior.set_color(Color.WARRIOR_COLORS.value[i])

    def is_round_ended(self):
        # TODO Support testing warriors with only one warrior in core
        return len(self.get_alive_warriors()) <= 1

    def get_alive_warriors(self):
        """
        Return list of warriors which have at least one process
        :return: Alive warrior count
        """
        return [warrior for warrior in self._warriors if warrior.processes()]

    def update_round_results(self):
        """
        Check if warriors is alive and increment its wins or loses
        """
        alive_warriors = self.get_alive_warriors()
        for warrior in self._warriors:
            info = warrior.warrior_info()
            info.inc_wins() if warrior in alive_warriors else info.inc_loses()

    def simulation_step(self):
        """
        Iterates all warriors and execute one queued instruction for each warrior
        """
        for warrior in self._warriors:
            if warrior.processes():
                instruction_pos = warrior.processes().pop(0)
                instruction = self._core[instruction_pos]
                instruction.execute(self._core, instruction_pos, warrior)
                # TODO Fill current executed instruction with color
                # self._gui.set_block_color(instruction_pos, Color.CURRENT_INSTRUCTION.value)
