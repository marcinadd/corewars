from enum import Enum

from src.enum.event import CoreEvent
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

    def get_core_address_mode_value(self, mode, value, instruction_pos, warrior):
        """
        Get indirect pointer to referenced instruction
        :param mode: Address mode
        :param value: Address value
        :param instruction_pos:
        :param warrior: Warrior which execute instruction
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
        self._check_predecrement(mode, value, warrior)
        # Indirect addressing
        if mode in (Mode.A_INDIRECT, Mode.A_PRE_DEC_INDIRECT, Mode.A_POST_INC_INDIRECT):
            return self[position].a_value() + value
        elif mode in (Mode.B_INDIRECT, Mode.B_PRE_DEC_INDIRECT, Mode.B_POST_INC_INDIRECT):
            return self[position].b_value() + value

    def _check_predecrement(self, mode, position, warrior):
        """
        Private method; checks if mode is predecrement and perform predecrement if necessary
        :param mode: Instruction mode
        :param position: Instruction position
        :param warrior: Warrior which executed this instruction
        """
        if mode == Mode.A_PRE_DEC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.A, -1)
            self.update_core_gui(position, warrior, CoreEvent.WRITE)
        elif mode == Mode.B_PRE_DEC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.B, -1)
            self.update_core_gui(position, warrior, CoreEvent.WRITE)

    def check_postincrement(self, mode, value, instruction_pos, warrior):
        """
            Checks if mode is postincrement and perform postincrement if necessary
            :param mode: Instruction mode
            :param value: Instruction operand value
            :param instruction_pos: Instruction position
            :param warrior: Warrior which executed this instruction
        """
        position = instruction_pos + value
        if mode == Mode.A_POST_INC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.A, 1)
            self.update_core_gui(position, warrior, CoreEvent.WRITE)
        elif mode == Mode.B_POST_INC_INDIRECT:
            self._add_value_to_core_instruction_field(position, FieldLetter.B, 1)
            self.update_core_gui(position, warrior, CoreEvent.WRITE)

    def _add_value_to_core_instruction_field(self, position, field_letter, change):
        """
        Adds "change" to instruction at "position"
        :param position: Instruction position in core
        :param field_letter: FieldLetter.A or FieldLetter.B; adds to first field or second
        :param change: Value to add
        """
        instruction = self[position]
        if field_letter == FieldLetter.A:
            # Adds change to instruction field A
            value = instruction.a_value() + change
            instruction.set_a_value(value)
        elif field_letter == FieldLetter.B:
            # Adds change to instruction field B
            value = instruction.b_value() + change
            instruction.set_b_value(value)

    def update_core_gui(self, block_number, warrior, event):
        """
        Sends event to core to update block at block_number
        :param block_number: Block number to be updated
        :param warrior: Warrior which executes event
        :param event: Event type
        """
        if self._gui:
            block_number = self.get_address_mod_core_size(block_number)
            self._gui.set_block_color(block_number, warrior.color(), event)

    def size(self):
        return self._size
