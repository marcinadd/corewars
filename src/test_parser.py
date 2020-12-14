from io import StringIO

from src.parser import parse_warrior


def test_parse_simple_instructions():
    data = """
            ADD.AB #4, 3
            MOV.I  2, @2
            JMP    -2 ; Useless comment for parsing test
            DAT    #0, #0
        """
    file_handle = StringIO(data)
    warrior = parse_warrior(file_handle)


test_parse_simple_instructions()
