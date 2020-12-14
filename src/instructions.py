from src.mode import Mode
from src.modifier import Modifier


class Instruction:
    def __init__(self, modifier, a_mode, a_value, b_mode, b_value):
        self._modifier = Modifier(modifier) if modifier else Modifier.AB
        self._a_mode = Mode(a_mode) if a_mode else Mode.DIRECT
        self._a_value = a_value
        self._b_mode = Mode(b_mode) if b_mode else Mode.DIRECT
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


class DAT(Instruction):
    pass


class MOV(Instruction):
    pass


class ArithmeticInstruction(Instruction):
    pass


class ADD(ArithmeticInstruction):
    pass
