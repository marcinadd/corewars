from src.instructions import Instruction, DAT
from src.mode import Mode
from src.modifier import Modifier


def test_instruction_create():
    instruction = Instruction('AB', '#', 1, '@', -1)
    assert instruction.modifier() == Modifier.AB
    assert instruction.a_mode() == Mode.IMMEDIATE
    assert instruction.a_value() == 1
    assert instruction.b_mode() == Mode.B_INDIRECT
    assert instruction.b_value() == -1


def test_instruction_str():
    instruction = DAT('AB', '#', 1, '@', -1)
    assert str(instruction) == 'DAT.AB #1, @-1'
