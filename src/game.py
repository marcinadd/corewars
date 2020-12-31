from src.gui.colors import Color
from src.round import Round


class Game:
    def __init__(self, warriors, core_size=8000, gui=None, rounds=10):
        self._core_size = core_size
        self._warriors = warriors
        self._rounds = rounds
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
        for round_num in range(1, self._rounds + 1):
            round_obj = Round(self._warriors, core_size=self._core_size, gui=self._gui, number=round_num)
            round_obj.play()
