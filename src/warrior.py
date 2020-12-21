from src.gui.colors import Color


class Warrior:
    def __init__(self, instructions=None, processes=None, color=Color.WARRIOR_DEFAULT.value):
        """

        :param instructions: Warrior instruction list; Optional to simplify testing
        :param processes: Init warrior with queued processes for testing purposes
        """
        self._instructions = instructions if instructions else []
        self._processes = processes if processes else []
        self._color = color

    def instructions(self):
        return self._instructions

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
