import copy

from src.core import Core
from src.enum.event import CoreEvent


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
        Iterates all warriors and load them into core
        """
        for warrior in self._warriors:
            # TODO Randomize warrior location here
            self._init_warrior(warrior, 540)

    def has_alive_warriors(self):
        """
        Check if game as any alive warrior
        :return: True if is any alive warrior else false
        """
        for warrior in self._warriors:
            if warrior.processes():
                return True
        return False

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
