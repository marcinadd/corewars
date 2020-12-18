from abc import abstractmethod, ABC
from copy import copy
from enum import Enum

from src.enum.mode import Mode
from src.enum.modifier import Modifier


class Instruction(ABC):
    def __init__(self, modifier, a_mode, a_value, b_mode, b_value):
        """
        Instruction constructor
        :param modifier: String modifier; for example "AB"
        :param a_mode: String a_mode; for example "#"
        :param a_value: String a_value; for example "-1"
        :param b_mode: String b_mode; for example "#"
        :param b_value: String b_value; for example "-1"
        """
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
        """
        Executes instruction in core
        :param core: Core object
        :param position: Instruction position in core addressing mode
        :param warrior: Warrior object to queue next task
        """
        a_pointer = core.get_core_address_mode_value(self._a_mode, self._a_value, position)
        b_pointer = core.get_core_address_mode_value(self._b_mode, self._b_value, position)
        a = copy(core[a_pointer + position])
        b = copy(core[b_pointer + position])

        # Postincrement (if necessary) after copy instruction
        core.check_postincrement(self._a_mode, self._a_value, position)
        core.check_postincrement(self._b_mode, self._b_value, position)

        core.update_core_gui(a_pointer + position, warrior)
        core.update_core_gui(b_pointer + position, warrior)

        self.instruction(a, b, a_pointer, b_pointer, position, core, warrior)

    @abstractmethod
    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        """
        Instruction to override in subclasses
        :param a: A instruction
        :param b: B instruction
        :param a_pointer: A instruction pointer relative to position
        :param b_pointer: B instruction pointer relative to position
        :param position: Position of current instruction in core
        :param core: Core object
        :param warrior: Warrior object to queue next task
        :return:
        """
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
    """
    Data (kills the process)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        pass


class MOV(Instruction):
    """
    Move (copies data from one address to another)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        modify_position = position + b_pointer
        if self._modifier == Modifier.I:
            core[modify_position] = a

        warrior.add_process(position + 1)


class ArithmeticOperator(Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    MODULO = '%'


def evaluate_expression(a, operator, b):
    """
    Evaluate mathematical expression; for example 2 / 3
    :param a: A value
    :param operator: ArithmeticOperator
    :param b: B value
    :return: Result of A op B
    """
    return eval(str(a) + operator.value + str(b))


class ArithmeticInstruction(Instruction):
    """
    Base class for arithmetic expressions
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        modify_position = position + b_pointer
        instruction_to_modify = core[modify_position]
        operator = self.get_operator()
        if self._modifier == Modifier.AB:
            expression_result = evaluate_expression(b.b_value(), operator, a.a_value())
            instruction_to_modify.set_b_value(expression_result)

        warrior.add_process(position + 1)

    def get_operator(self):
        # Implemented in extending classes
        return ArithmeticOperator.ADD  # Set default to fix linter errors


class ADD(ArithmeticInstruction):
    """
    Add (adds one number to another)
    """

    def get_operator(self):
        return ArithmeticOperator.ADD


class SUB(ArithmeticInstruction):
    """
    Subtract (subtracts one number from another)
    """

    def get_operator(self):
        return ArithmeticOperator.SUBTRACT


class JMP(Instruction):
    """
    Jump (continues execution from another address)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        warrior.add_process(position + a_pointer)


class SPL(Instruction):
    """
    Split (starts a second process at another address)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        warrior.add_process(position + 1)
        warrior.add_process(position + a_pointer)
