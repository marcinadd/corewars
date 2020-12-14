import copy

from src.core import Core


class Game:
    def __init__(self, warriors=None, core_size=200):
        self._core = Core(core_size)
        self._warriors = warriors if warriors else []

    def _init_warrior(self, warrior, starting_core_address):
        self._core[starting_core_address] = copy.copy(warrior.instructions())
        for offset, instruction in warrior.instructions():
            self._core[starting_core_address + offset] = copy.copy(instruction)

    def init_warriors(self):
        for warrior in self._warriors:
            # TODO Randomize warrior location here
            self._init_warrior(warrior, 0)
