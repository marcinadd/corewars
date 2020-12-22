from abc import abstractmethod, ABC
from copy import copy
from enum import Enum

from src.enum.event import CoreEvent
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
        self._modifier = Modifier(modifier.upper()) if modifier else Modifier.AB
        self._a_mode = Mode(a_mode.upper()) if a_mode else Mode.DIRECT
        self._a_value = int(a_value) if a_value else 0
        self._b_mode = Mode(b_mode.upper()) if b_mode else Mode.DIRECT
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
        a_pointer = core.get_core_address_mode_value(self._a_mode, self._a_value, position, warrior)
        a = copy(core[a_pointer + position])
        core.check_postincrement(self._a_mode, self._a_value, position, warrior)

        b_pointer = core.get_core_address_mode_value(self._b_mode, self._b_value, position, warrior)
        b = copy(core[b_pointer + position])
        core.check_postincrement(self._b_mode, self._b_value, position, warrior)

        result = self.instruction(a, b, a_pointer, b_pointer, position, core, warrior)
        core.update_core_gui(position + a_pointer, warrior, CoreEvent.EXECUTE)
        if result is not None:
            event_a, event_b = result
            if event_a:
                core.update_core_gui(position + a_pointer, warrior, event_a)
            if event_b:
                core.update_core_gui(position + b_pointer, warrior, event_b)

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

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and self.modifier() == other.modifier() and
                self.a_mode() == other.a_mode() and self.a_value() == other.a_value() and
                self.b_mode() == other.b_mode() and self.b_value() == other.b_value()
        )


class DAT(Instruction):
    """
    Data (kills the process)
    """

    def __init__(self, modifier, a_mode, a_value, b_mode, b_value):
        if b_value:
            super(DAT, self).__init__(modifier, a_mode, a_value, b_mode, b_value)
        else:
            # When only one operand given it should be parsed as b operand
            super(DAT, self).__init__(modifier, Mode.DIRECT.value, 0, a_mode, a_value)

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        pass


class MOV(Instruction):
    """
    Move (copies data from one address to another)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        modify_position = position + b_pointer
        result = (None, None)
        if self._modifier == Modifier.A:
            core[modify_position].set_a_value(a.a_value())
        elif self._modifier == Modifier.B:
            core[modify_position].set_b_value(a.b_value())
        elif self._modifier == Modifier.AB:
            core[modify_position].set_b_value(a.a_value())
        elif self._modifier == Modifier.BA:
            core[modify_position].set_a_value(a.b_value())
        elif self._modifier == Modifier.F:
            core[modify_position].set_a_value(a.a_value())
            core[modify_position].set_b_value(a.b_value())
        elif self._modifier == Modifier.X:
            core[modify_position].set_a_value(a.b_value())
            core[modify_position].set_b_value(a.a_value())
        elif self._modifier == Modifier.I:
            core[modify_position] = a
            result = CoreEvent.READ, CoreEvent.WRITE
        warrior.add_process(position + 1)
        return result


class ArithmeticOperator(Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    MODULO = '%'


class ComparisonOperator(Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LOWER_THAN = "<"


def eval_expression(a, operator, b):
    """
    Evaluate mathematical or compare expression; for example 2 / 3
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
        try:
            modify_position = position + b_pointer
            instruction_to_modify = core[modify_position]
            operator = self.get_operator()
            if self._modifier == Modifier.A:
                instruction_to_modify.set_a_value(eval_expression(b.a_value(), operator, a.a_value()))
            elif self._modifier == Modifier.B:
                instruction_to_modify.set_b_value(eval_expression(b.b_value(), operator, a.b_value()))
            elif self._modifier == Modifier.AB:
                instruction_to_modify.set_b_value(eval_expression(b.b_value(), operator, a.a_value()))
            elif self._modifier == Modifier.BA:
                instruction_to_modify.set_a_value(eval_expression(b.b_value(), operator, a.a_value()))
            elif self._modifier in (Modifier.F, Modifier.I):
                instruction_to_modify.set_a_value(eval_expression(b.a_value(), operator, a.a_value()))
                instruction_to_modify.set_b_value(eval_expression(b.b_value(), operator, a.b_value()))
            elif self._modifier == Modifier.X:
                instruction_to_modify.set_a_value(eval_expression(b.a_value(), operator, a.b_value()))
                instruction_to_modify.set_b_value(eval_expression(b.b_value(), operator, a.a_value()))

            warrior.add_process(position + 1)
        except ZeroDivisionError:
            # Kill warrior process
            pass

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


class MUL(ArithmeticInstruction):
    """
       Multiply (multiplies one number with another)
    """

    def get_operator(self):
        return ArithmeticOperator.MULTIPLY


class DIV(ArithmeticInstruction):
    """
       Divide (divides one number with another)
    """

    def get_operator(self):
        return ArithmeticOperator.DIVIDE


class MOD(ArithmeticInstruction):
    """
       Modulus (divides one number with another and gives the remainder)
    """

    def get_operator(self):
        return ArithmeticOperator.MODULO


class JMP(Instruction):
    """
    Jump (continues execution from another address)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        warrior.add_process(position + a_pointer)


class JMZ(Instruction):
    """
    Jump if zero (tests a number and jumps to an address if it's 0)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        jump = 1
        if self._modifier in (Modifier.A, Modifier.BA):
            jump = a_pointer if a.a_value() == 0 else 1
        elif self._modifier in (Modifier.B, Modifier.AB):
            jump = a_pointer if a.b_value() == 0 else 1
        elif self._modifier in (Modifier.F, Modifier.X, Modifier.I):
            jump = a_pointer if a.a_value() == 0 and a.b_value() == 0 else 1
        warrior.add_process(position + jump)


class JMN(Instruction):
    """
    Jump if not zero (tests a number and jumps if it isn't 0)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        jump = 1
        if self._modifier in (Modifier.A, Modifier.BA):
            jump = a_pointer if a.a_value() != 0 else 1
        elif self._modifier in (Modifier.B, Modifier.AB):
            jump = a_pointer if a.b_value() != 0 else 1
        elif self._modifier in (Modifier.F, Modifier.X, Modifier.I):
            jump = a_pointer if a.a_value() != 0 or b.b_value() != 0 else 1
        warrior.add_process(position + jump)


class DJN(JMN):
    """
    Decrement and jump if not zero (decrements a number by one, and jumps unless the result is 0)
    """

    @staticmethod
    def _decrement_a(instruction, a):
        decremented_a = instruction.a_value() - 1
        instruction.set_a_value(decremented_a)
        a.set_a_value(decremented_a)

    @staticmethod
    def _decrement_b(instruction, a):
        decremented_b = instruction.b_value() - 1
        instruction.set_a_value(decremented_b)
        a.set_b_value(decremented_b)

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        instruction_to_decrement = core[position + a_pointer]
        if self._modifier in (Modifier.A, Modifier.BA):
            self._decrement_a(instruction_to_decrement, a)
        elif self._modifier in (Modifier.B, Modifier.AB):
            self._decrement_a(instruction_to_decrement, b)
        elif self._modifier in (Modifier.F, Modifier.X, Modifier.I):
            self._decrement_a(instruction_to_decrement, a)
            self._decrement_b(instruction_to_decrement, a)
        super(DJN, self).instruction(a, b, a_pointer, b_pointer, position, core, warrior)


class SPL(Instruction):
    """
    Split (starts a second process at another address)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        warrior.add_process(position + 1)
        warrior.add_process(position + a_pointer)


class CompareAndSkipInstruction(Instruction):
    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        operator = self.get_operator()
        skip = False
        result = (None, None)
        if self._modifier == Modifier.A:
            skip = eval_expression(a.a_value(), operator, b.a_value())
        elif self._modifier == Modifier.B:
            skip = eval_expression(a.b_value(), operator, b.b_value())
        elif self._modifier == Modifier.AB:
            skip = eval_expression(a.a_value(), operator, b.b_value())
        elif self._modifier == Modifier.BA:
            skip = eval_expression(a.b_value(), operator, b.a_value())
        elif self._modifier == Modifier.F:
            first = eval_expression(a.a_value(), operator, b.a_value())
            second = eval_expression(a.b_value(), operator, b.b_value())
            skip = first and second
        elif self._modifier == Modifier.X:
            first = eval_expression(a.a_value(), operator, b.b_value())
            second = eval_expression(a.b_value(), operator, b.a_value())
            skip = first and second
        elif self._modifier == Modifier.I:
            skip = a == b
            result = (CoreEvent.READ, CoreEvent.READ)

        next_instruction = position + (2 if skip else 1)
        warrior.add_process(next_instruction)
        return result

    def get_operator(self):
        # Implemented in extending classes
        return ComparisonOperator.EQUAL  # Set default to fix linter errors


class SEQ(CompareAndSkipInstruction):
    """
    Skip if equal (compares two instructions, and skips the next instruction if they are equal)
    """

    def get_operator(self):
        return ComparisonOperator.EQUAL


class SNE(CompareAndSkipInstruction):
    """
    Skip if not equal (compares two instructions, and skips the next instruction if they aren't equal)
    """

    def get_operator(self):
        return ComparisonOperator.NOT_EQUAL


class SLT(CompareAndSkipInstruction):
    """
    Skip if lower than (compares two values, and skips the next instruction if the first is lower than the second)
    """

    def get_operator(self):
        return ComparisonOperator.LOWER_THAN


class NOP(Instruction):
    """
    No operation (does nothing)
    """

    def instruction(self, a, b, a_pointer, b_pointer, position, core, warrior):
        warrior.add_process(position + 1)
