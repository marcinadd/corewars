from src.enum.mode import Mode
from src.instructions import DAT


def prepare_core(size):
    """
    Fills core with values
    :param size: Core size
    :return:
    """
    return [DAT('F', '$', 0, '$', 0) for _ in range(size)]


class Core:
    def __init__(self, size=250, data=None):
        """
        :param size: Optional for custom core size
        :param data: Optional param Use predefined core data; Useful for testing
        """
        self._size = size if not data else len(data)
        self._data = data if data else prepare_core(size)

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
            # Instruction address to current position
            return value
        elif mode == Mode.A_INDIRECT:
            position = instruction_pos + value
            return self._data[position].a_value() + value
        elif mode == Mode.B_INDIRECT:
            position = instruction_pos + value
            return self._data[position].b_value() + value
