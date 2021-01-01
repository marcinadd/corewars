import re

from src.instructions import *
from src.warrior import Warrior


class InvalidInstructionCodeException(Exception):
    def __init__(self, instruction_code):
        super().__init__(f'Invalid instruction code {instruction_code}')


class InvalidInstructionSyntaxException(Exception):
    def __init__(self, line, line_number):
        super().__init__(f'Invalid syntax in line {line_number}: {line}')


INSTRUCTION_PATTERN = re.compile(r'^([A-Z]{3})'  # INSTRUCTION
                                 r'(?:\.(AB|BA|[ABFXI]))?'  # MODIFIER
                                 r'(?:\s+([#$*@{<}>])?([^\s,;]+))'  # A-MODE, A-VALUE
                                 r'(?:\s*,\s*([#$*@{<}>])?([^\s]+)\s*)?'  # B-MODE, B-VALUE
                                 r'(?:\s*;.*)?$'  # Non capturing optional comment
                                 )
NAME_PATTERN = re.compile(r'^(?:;name\s*(.*))$')

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


def parse_instruction(line, line_number=1):
    """
    Parses single warrior instruction
    :param line: Line to parse
    :param line_number: Line number for error reporting
    :return: A class which extends Instruction abstract class
    """
    match = re.search(INSTRUCTION_PATTERN, line.upper())
    if not match:
        raise InvalidInstructionSyntaxException(line, line_number)
    groups = list(match.groups())
    instruction_code = groups[0]
    instruction_values = groups[1:]
    if instruction_code in INSTRUCTION_CODES:
        instruction_class = INSTRUCTION_CODES[instruction_code]
        instruction = instruction_class(*instruction_values)
        return instruction
    else:
        raise InvalidInstructionCodeException(instruction_code)


def try_parse_name(line):
    """
    Checks if line contains warrior name and parses it
    :param line: Line string
    :return: Warrior name or None
    """
    match = re.search(NAME_PATTERN, line)
    return list(match.groups())[0] if match else None


def parse_warrior(file_handle):
    """
    Parses warrior instructions from file_handle
    :param file_handle: file_handle stream
    :return: warrior object
    """
    instructions = []
    name = None
    for line_number, line in enumerate(file_handle):
        line = line.strip()
        if line:
            if line.startswith(';'):
                # It is comment
                # Try to parse it as name comment
                parsed_name = try_parse_name(line)
                if parsed_name:
                    # Set warrior name
                    name = parsed_name
            else:
                # It isn't a comment and should be parsed as instruction
                instruction = parse_instruction(line, line_number)
                instructions.append(instruction)

    return Warrior(instructions, name=name)
