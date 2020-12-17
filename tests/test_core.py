from src.core import Core
from src.instructions import DAT, ADD


def test_get_cycled_value_begin():
    instruction_1 = DAT('F', '$', 1, '$', 5)
    instruction_2 = ADD('AB', '#', '3', '$', '-2')
    instruction_3 = DAT('F', '$', 1, '$', -5)
    core = Core(data=[instruction_1, instruction_2, instruction_3])
    assert core[-5] == instruction_2


def test_get_cycled_value_end():
    instruction_1 = DAT('F', '$', 1, '$', 5)
    instruction_2 = ADD('AB', '#', '3', '$', '-2')
    instruction_3 = DAT('F', '$', 1, '$', -5)
    core = Core(data=[instruction_1, instruction_2, instruction_3])
    assert core[5] == instruction_3
