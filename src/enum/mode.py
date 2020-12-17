from enum import Enum


class Mode(Enum):
    IMMEDIATE = '#'
    DIRECT = '$'
    A_INDIRECT = '*'
    B_INDIRECT = '@'
    A_PRE_DEC_INDIRECT = "{"
    A_POST_INC_INDIRECT = "}"
    B_PRE_DEC_INDIRECT = "<"
    B_POST_INC_INDIRECT = ">"
