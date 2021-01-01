from src.gui.colors import Color

WARRIOR_DEFAULT_NAME = "Warrior"


class Warrior:
    def __init__(self, instructions=None, processes=None, color=Color.WARRIOR_DEFAULT.value, name=None):
        """

        :param instructions: Warrior instruction list; Optional to simplify testing
        :param processes: Init warrior with queued processes for testing purposes
        """
        self._instructions = instructions if instructions else []
        self._processes = processes if processes else []
        self._color = color
        self._warrior_info = WarriorInfo(name if name else WARRIOR_DEFAULT_NAME)

    def add_process(self, position):
        """
        Adds process to warrior processes queue list
        :param position:int: Address in core
        """
        self._processes.append(position)

    def processes(self):
        return self._processes

    def color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def warrior_info(self):
        return self._warrior_info

    def instructions(self):
        return self._instructions


class WarriorInfo:
    """
    Warrior details name, wins, ties, loses for game results
    """

    def __init__(self, name):
        """
        :param name:
        """
        self._name = name
        self._wins = 0
        self._ties = 0
        self._loses = 0

    def inc_wins(self):
        self._wins += 1

    def inc_ties(self):
        self._ties += 1

    def inc_loses(self):
        self._loses += 1

    def wins(self):
        return self._wins

    def ties(self):
        return self._ties

    def loses(self):
        return self._loses

    def name(self):
        return self._name
