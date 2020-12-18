from enum import Enum

from src.enum.mode import Mode
from src.instructions import DAT


def prepare_core(size):
    """
    Generate data with single instruction
    :param size: Core size
    :return: Core data
    """
    return [DAT('F', '$', 0, '$', 0) for _ in range(size)]


class FieldLetter(Enum):
    A = 'A'
    B = 'B'


class Core:
    def __init__(self, size=250, data=None, gui=None):
        """
        :param size: Optional for custom core size
        :param data: Optional param Use predefined core data; Useful for testing
        """
        self._size = size if not data else len(data)
        self._data = data if data else prepare_core(size)
        self._gui = gui

    def __getitem__(self, item):
        address = self.get_address_mod_core_size(item)
        return self._data[address]

    def __setitem__(self, key, value):
        address = self.get_address_mod_core_size(key)
        self._data[address] = value

    def get_address_mod_core_size(self, address):
        """
        Get cycled address
        :param address: 
        :return: Address which fit in core
        """
        return address % self._size

    def get_core_address_mode_value(self, mode, value, instruction_pos):
        """
        Get indirect pointer to referenced instruction
        :param mode: Address mode
        :param value: Address value
        :param instruction_pos:
        :return: Indirect pointer to referenced instruction
        """
        if mode == Mode.IMMEDIATE:
            # Pointer is 0
            return 0
        if mode == Mode.DIRECT:
            # Direct address to current position
            return value

        position = instruction_pos + value
        # Predecrement (if necessary)
        self._check_predecrement(mode, value)
        # Indirect addressing
        address = 0
        if mode in (Mode.A_INDIRECT, Mode.A_PRE_DEC_INDIRECT, Mode.A_POST_INC_INDIRECT):
            return self[position].a_value()
        elif mode in (Mode.B_INDIRECT, Mode.B_PRE_DEC_INDIRECT, Mode.B_POST_INC_INDIRECT):
            return self[position].b_value()

    def _check_predecrement(self, mode, position):
        if mode == Mode.A_PRE_DEC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.A, -1)
        elif mode == Mode.B_PRE_DEC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.B, -1)

    def check_postincrement(self, mode, value, instruction_pos):
        position = instruction_pos + value
        if mode == Mode.A_POST_INC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.A, 1)
        elif mode == Mode.B_POST_INC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.B, 1)

    def _add_value_to_core_instruction_field(self, position, field_letter, change):
        instruction = self[position]
        if field_letter == FieldLetter.A:
            # Adds change to instruction field A
            value = instruction.a_value() + change
            instruction.set_a_value(value)
        elif field_letter == FieldLetter.B:
            # Adds change to instruction field B
            value = instruction.b_value() + change
            instruction.set_b_value(value)

    def update_core_gui(self, block_number, warrior):
        if self._gui:
            block_number = self.get_address_mod_core_size(block_number)
            self._gui.set_block_color(block_number, warrior.color())
