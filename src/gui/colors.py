from enum import Enum


class Color(Enum):
    BACKGROUND = (0, 0, 0)
    GRAY = (150, 150, 150)
    WARRIOR_DEFAULT = (255, 0, 0)
    CURRENT_INSTRUCTION = (255, 255, 255)
    WARRIOR_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    TEXT_COLOR = (255, 255, 255)
