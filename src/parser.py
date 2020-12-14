import re

from src.warrior import Warrior

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
            print(line)

    return Warrior(instructions)
