from src.warrior import Warrior


def parse_warrior(file_handle):
    instructions = []
    for line in file_handle:
        line = line.strip().upper()
        if line:
            print(line)

    return Warrior(instructions)
