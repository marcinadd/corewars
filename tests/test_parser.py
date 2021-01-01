from io import StringIO

import pytest

from src.instructions import *
from src.parser import InvalidInstructionCodeException, InvalidInstructionSyntaxException
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


def test_parse_warrior_name():
    data = ";name Imp"
    file_handle = StringIO(data)
    warrior = parse_warrior(file_handle)
    assert warrior.warrior_info().name() == "Imp"


def test_parse_warrior_skip_blank_lines():
    data = """
                    ADD.AB #4, 3
                    
                    MOV.I  2, @2
    """
    file_handle = StringIO(data)
    warrior = parse_warrior(file_handle)
    instructions = warrior.instructions()
    assert len(instructions) == 2


def test_parse_warrior_skip_comment_lines():
    data = """  ; This is comment line
                ADD.AB #4, 3
                ; Another comment
                 MOV.I  2, @2
    """
    file_handle = StringIO(data)
    warrior = parse_warrior(file_handle)
    instructions = warrior.instructions()
    assert len(instructions) == 2


def test_parse_warrior_invalid_instruction_code():
    data = "XYZ.AB #4, 3"
    file_handle = StringIO(data)
    with pytest.raises(InvalidInstructionCodeException):
        parse_warrior(file_handle)


def test_parse_warrior_invalid_instruction_syntax():
    data = "INVALID.AB ERR"
    file_handle = StringIO(data)
    with pytest.raises(InvalidInstructionSyntaxException):
        parse_warrior(file_handle)
