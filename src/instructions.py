from copy import copy

from src.mode import Mode
from src.modifier import Modifier


class Instruction:
    def __init__(self, modifier, a_mode, a_value, b_mode, b_value):
        self._modifier = Modifier(modifier) if modifier else Modifier.AB
        self._a_mode = Mode(a_mode) if a_mode else Mode.DIRECT
        self._a_value = int(a_value) if a_value else 0
        self._b_mode = Mode(b_mode) if b_mode else Mode.DIRECT
        self._b_value = int(b_value) if b_value else 0

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

    def set_a_value(self, a_value):
        self._a_value = a_value

    def set_b_value(self, b_value):
        self._b_value = b_value

    def execute(self, core, position, warrior):
        a_pointer = core.get_core_address_mode_value(self._a_mode, self._a_value, position)
        b_pointer = core.get_core_address_mode_value(self._b_mode, self._b_value, position)
        a = copy(core[a_pointer + position])
        b = copy(core[b_pointer + position])

        self.instruction(a, b, a_pointer, b_pointer, position, core, warrior)

    #     TODO Post dec/post inc here

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        # Override when extending
        pass

    def __str__(self):
        name = type(self).__name__.upper()
        modifier = self._modifier.value
        a_mode = self._a_mode.value
        a_value = self._a_value
        b_mode = self._b_mode.value
        b_value = self._b_value
        return f'{name}.{modifier} {a_mode}{a_value}, {b_mode}{b_value}'


class DAT(Instruction):
    pass


class MOV(Instruction):
    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        modify_position = position + b_pointer
        if self._modifier == Modifier.I:
            core[modify_position] = a

        warrior.add_process(position + 1)


def evaluate_expression(a, operator, b):
    return eval(str(a) + operator + str(b))


class ArithmeticInstruction(Instruction):
    pass


class ADD(ArithmeticInstruction):
    pass
