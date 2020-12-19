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

INSTRUCTION_CODES = {
    "DAT": DAT,
    "MOV": MOV,
    "ADD": ADD,
    "SUB": SUB,
    "MUL": MUL,
    "DIV": DIV,
    "MOD": MOD,
    "JMP": JMP,
    "JMZ": JMZ,
    "JMN": JMN,
    "DJN": DJN,
    "SEQ": SEQ,
    "SNE": SNE,
    "SLT": SLT,
    "SPL": SPL,
    "NOP": NOP
}


def parse_warrior(file_handle):
    """
    Parses warrior instructions from file_handle
    :param file_handle: file_handle stream
    :return: warrior object
    """
    instructions = []
    for line in file_handle:
        line = line.strip().upper()
        if line:
            match = re.search(INSTRUCTION_PATTERN, line)
            groups = list(match.groups())
            instruction_code = groups[0]
            instruction_values = groups[1:]
            if instruction_code in INSTRUCTION_CODES:
                instruction_class = INSTRUCTION_CODES[instruction_code]
                instruction = instruction_class(*instruction_values)
                instructions.append(instruction)
            else:
                raise InvalidInstructionException(instruction_code)
    return Warrior(instructions)
