class Warrior:
    def __init__(self, instructions):
        self._instructions = instructions
        self._processes = []

    def instructions(self):
        return self._instructions

    def add_process(self, position):
        self._processes.append(position)

    def processes(self):
        return self._processes
