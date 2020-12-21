import glob

from src.parser import parse_warrior

DEFAULT_WARRIORS_DIRECTORY = "warriors/"


def get_warrior_files(directory=DEFAULT_WARRIORS_DIRECTORY):
    return glob.glob(directory + "*.red")


def get_warrior_list(warrior_files):
    if warrior_files:
        # Load warriors from specified files
        paths = warrior_files
    else:
        # Load warriors from default directory
        paths = get_warrior_files()
    warriors = []
    for path in paths:
        with open(path, 'r') as file_handle:
            warrior = parse_warrior(file_handle)
            warriors.append(warrior)

    return warriors
