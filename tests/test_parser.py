from io import StringIO

from src.instructions import *
from src.parser import parse_warrior


def test_parse_warrior_instructions_classes():
    data = """
                ADD.AB #4, 3
                MOV.I  2, @2
                JMP    -2 ; Useless comment for parsing test
                DAT    #0, #0
            """
    file_handle = StringIO(data)
    warrior = parse_warrior(file_handle)
    instructions = warrior.instructions()
    assert len(instructions) == 4
    assert type(warrior.instructions()[0]) is ADD
    assert type(warrior.instructions()[1]) is MOV
    assert type(warrior.instructions()[2]) is JMP
    assert type(warrior.instructions()[3]) is DAT


def test_parse_instruction_data():
    data = "ADD.AB #-4, $3"
    file_handle = StringIO(data)
    warrior = parse_warrior(file_handle)
    first_instruction = warrior.instructions()[0]
    assert first_instruction.modifier() == Modifier.AB
    assert first_instruction.a_mode() == Mode.IMMEDIATE
    assert first_instruction.a_value() == -4
    assert first_instruction.b_mode() == Mode.DIRECT
    assert first_instruction.b_value() == 3
