class Warrior:
    def __init__(self, instructions=None, processes=None):
        """

        :param instructions: Warrior instruction list; Optional to simplify testing
        :param processes: Init warrior with queued processes for testing purposes
        """
        self._instructions = instructions if instructions else []
        self._processes = processes if processes else []

    def instructions(self):
        return self._instructions

    def add_process(self, position):
        self._processes.append(position)

    def processes(self):
        return self._processes
