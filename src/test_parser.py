from io import StringIO

from src.instructions import *
from src.parser import parse_warrior


def test_parse_warrior_instructions():
    data = """
                MOV.I  2, @2
                DAT    #0, #0
                DAT    #0, #1
            """
    file_handle = StringIO(data)
    warrior = parse_warrior(file_handle)
    instructions = warrior.instructions()
    assert len(instructions) == 3
    assert type(warrior.instructions()[0]) is MOV
    assert type(warrior.instructions()[1]) is DAT


def test_parse_simple_instructions():
    data = """
            ADD.AB #4, 3
            MOV.I  2, @2
            JMP    -2 ; Useless comment for parsing test
            DAT    #0, #0
        """
    file_handle = StringIO(data)
    # warrior = parse_warrior(file_handle)
