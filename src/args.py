import argparse


class IntBetween:
    def __init__(self, minim, maxim):
        self._minim = minim
        self._maxim = maxim

    def __call__(self, arg):
        try:
            val = int(arg)
            if not self._minim <= val <= self._maxim:
                raise ValueError()
        except (TypeError, ValueError):
            raise argparse.ArgumentTypeError(f'Must be an integer in range [{self._minim},{self._maxim}]')
        return val


class InvalidNumberOfWarriorsException(Exception):
    def __init__(self, max_number):
        msg = f'Invalid number of warriors. Number of warriors should be in range [2,{max_number}]'
        super().__init__(msg)


def check_warrior_count(max_count):
    """
    Check if number of warriors is between [2, max_count] or zero
    :param max_count: Max number of warriors given in arguments
    :raises InvalidNumberOfWarriorsException
    """

    class CheckWarriorNumberAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            current_length = len(values)
            # Allow zero warriors args (default warriors will be loaded)
            # Disallow only one warrior or more arguments than max_count
            if current_length > max_count or current_length == 1:
                raise InvalidNumberOfWarriorsException(max_count)
            setattr(args, self.dest, values)

    return CheckWarriorNumberAction
