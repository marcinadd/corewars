import glob
import os
import random

from src.config import DEFAULT_WARRIORS_DIRECTORY, DEFAULT_WARRIOR_COUNT
from src.parser import parse_warrior


def get_warrior_files(directory=DEFAULT_WARRIORS_DIRECTORY):
    """
    Get all warriors files from given directory
    :param directory: Path
    :return: List of warriors file paths
    """
    return glob.glob(directory + "*.red")


def get_warrior_list(warrior_files):
    """
    Parse warriors from specified files or use default warriors directory
    :param warrior_files: List of warrior file paths
    :return: Warrior objects list
    """
    if warrior_files:
        # Load warriors from specified files
        paths = warrior_files
    else:
        # Load random warriors from default directory
        warrior_files = get_warrior_files()
        paths = random.sample(warrior_files, DEFAULT_WARRIOR_COUNT)

    warriors = []
    for path in paths:
        if os.path.isfile(path):
            with open(path, 'r') as file_handle:
                warrior = parse_warrior(file_handle)
                warriors.append(warrior)
    return warriors
