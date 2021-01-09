from argparse import ArgumentTypeError

import pytest

from src.intbetween import IntBetween


def test_int_between_ok():
    intbetween = IntBetween(1, 20)
    intbetween(1)
    intbetween(20)


def test_int_between_value_too_low():
    intbetween = IntBetween(1, 20)
    with pytest.raises(ArgumentTypeError):
        intbetween(0)


def test_int_between_value_too_high():
    intbetween = IntBetween(1, 20)
    with pytest.raises(ArgumentTypeError):
        intbetween(21)


def test_int_between_none():
    intbetween = IntBetween(1, 20)
    with pytest.raises(ArgumentTypeError):
        intbetween(None)


def test_int_between_not_int():
    intbetween = IntBetween(1, 20)
    with pytest.raises(ArgumentTypeError):
        intbetween('NotInt')
