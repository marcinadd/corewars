import copy

from src.core import Core


class Game:
    def __init__(self, warriors=None, core=None, core_size=200):
        self._core = core if Core else Core(core_size)
        self._warriors = warriors if warriors else []
        self.init_warriors()

    def core(self):
        return self._core

    def _init_warrior(self, warrior, starting_core_address):
        self._core[starting_core_address] = copy.copy(warrior.instructions())
        for offset, instruction in enumerate(warrior.instructions()):
            self._core[starting_core_address + offset] = copy.copy(instruction)
        warrior.add_process(starting_core_address)

    def init_warriors(self):
        for warrior in self._warriors:
            # TODO Randomize warrior location here
            self._init_warrior(warrior, 0)

    def simulation_step(self):
        for warrior in self._warriors:
            if warrior.processes():
                instruction_pos = warrior.processes().pop(0)
                instruction = self._core[instruction_pos]
                instruction.execute(self._core, instruction_pos, warrior)
