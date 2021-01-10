from src.gui.colors import Color
from src.round import Round


class Game:
    def __init__(self, warriors, core_size=8000, gui=None, rounds=10, max_cycles=80000):
        """
        Game constructor
        :param warriors: Warriors list
        :param core_size:  Optional core size
        :param gui: Optional Gui
        :param rounds: Number of rounds to play
        """
        self._core_size = core_size
        self._warriors = warriors
        self._rounds = rounds
        self._max_cycles = max_cycles
        if gui:
            self._gui = gui
            self._gui.init_game_screen()
            self._set_warriors_colors()

    def _set_warriors_colors(self):
        """
        Sets warrior colors from Color.WARRIOR_COLORS
        """
        for i, warrior in enumerate(self._warriors):
            warrior.set_color(Color.WARRIOR_COLORS.value[i])

    def play(self):
        """
        Play rounds
        """
        for round_num in range(1, self._rounds + 1):
            round_obj = Round(self._warriors, core_size=self._core_size, gui=self._gui, number=round_num,
                              max_cycles=self._max_cycles)
            round_obj.play()

    def get_results_string(self):
        """
        Get strings with results after finished game
        :return: Formatted string with warrior results
        """
        text = f'****Won-Lost-Tied after {self._rounds} round/s****\n'
        for warrior in self._warriors:
            info = warrior.warrior_info()
            text += f'{info.name()}: {info.wins()}-{info.loses()}-{info.ties()}\n'
        return text
