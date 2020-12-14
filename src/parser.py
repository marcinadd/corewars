import re

from src.instructions import *
from src.warrior import Warrior


class InvalidInstructionException(Exception):
    def __init__(self, instruction_code):
        super().__init__(f'Invalid instruction {instruction_code}')


INSTRUCTION_PATTERN = re.compile(r'^([A-Z]{3})'  # INSTRUCTION
                                 r'(?:\.(AB|BA|[ABFXI]))?'  # MODIFIER
                                 r'(?:\s+([#$*@{<}>])?([^\s,;]+))'  # A-MODE, A-VALUE
                                 r'(?:\s*,\s*([#$*@{<}>])?([^\s]+)\s*)?'  # B-MODE, B-VALUE
                                 r'(?:\s*;.*)?$'  # Non capturing optional comment
                                 )


def parse_warrior(file_handle):
    instructions = []
    for line in file_handle:
        line = line.strip().upper()
        if line:
            match = re.search(INSTRUCTION_PATTERN, line)
            instruction_code, modifier, a_mode, a_value, b_mode, b_value = match.groups()
            if instruction_code == "DAT":
                instruction = DAT(modifier, a_mode, a_value, b_mode, b_value)
            elif instruction_code == "MOV":
                instruction = MOV(modifier, a_mode, a_value, b_mode, b_value)
            elif instruction_code == "ADD":
                instruction = ADD(modifier, a_mode, a_value, b_mode, b_value)
            else:
                raise InvalidInstructionException(instruction_code)
            instructions.append(instruction)
    return Warrior(instructions)
