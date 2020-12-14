from src.mode import Mode
from src.modifier import Modifier


class Instruction:
    def __init__(self, modifier, a_mode, a_value, b_mode, b_value):
        self._modifier = Modifier(modifier)
        self._a_mode = Mode(a_mode)
        self._a_value = a_value
        self._b_mode = Mode(b_mode)
        self._b_value = b_value

    def modifier(self):
        return self._modifier

    def a_mode(self):
        return self._a_mode

    def a_value(self):
        return self._a_value

    def b_mode(self):
        return self._b_mode

    def b_value(self):
        return self._b_value
