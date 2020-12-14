from src.instructions import DAT
from src.mode import Mode


def prepare_core(size):
    return [DAT('F', '$', 0, '$', 0) for _ in range(size)]


class Core:
    def __init__(self, size=250):
        self._size = size
        self._data = prepare_core(size)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def get_value_mod_core_size(self, value):
        return value % self._size

    def get_core_address_mode_value(self, mode, value, instruction_pos):
        if mode == Mode.IMMEDIATE:
            # Reading value from core isn't necessary
            return value
        if mode == Mode.DIRECT:
            # Return position
            return self.get_value_mod_core_size(instruction_pos + value)
        elif mode == Mode.A_INDIRECT:
            position = self.get_value_mod_core_size(instruction_pos + value)
            return self._data[position].a_value()
        elif mode == Mode.B_INDIRECT:
            position = self.get_value_mod_core_size(instruction_pos + value)
            return self._data[position].b_value()
