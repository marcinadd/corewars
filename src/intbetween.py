import argparse


class IntBetween:
    def __init__(self, minim, maxim):
        self._minim = minim
        self._maxim = maxim

    def __call__(self, arg):
        try:
            val = int(arg)
            if val < self._minim or val > self._maxim:
                raise ValueError()
        except (TypeError, ValueError):
            raise argparse.ArgumentTypeError(f'Must be an integer in range [{self._minim},{self._maxim}]')
        return val
