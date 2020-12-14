from src.instructions import DAT


class Core:
    def __init__(self, size=250):
        self._size = size
        self._prepare()
        self._data = []
        self._prepare()

    def _prepare(self):
        for _ in range(self._size):
            self._data.append(DAT('F', '$', 0, '$', 0))
