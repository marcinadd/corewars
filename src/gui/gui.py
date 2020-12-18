import pygame

from src.gui.colors import Color


def divide_blocks(core_size):
    # TODO Dividing blocks
    return 100, 80


class GUI:
    def __init__(self, width, height, core_size):
        self._width = width
        self._height = height
        self._blocks_x, self._blocks_y = divide_blocks(core_size)
        self._core_size = core_size

    def init_game_screen(self):
        pass

    def draw_block(self, number, color):
        pass

    def get_block_position(self, block_number):
        y = block_number // self._blocks_x
        x = block_number % self._blocks_x
        return x, y


class PyGameGUI(GUI):
    def __init__(self, width, height, ticks=30, core_size=8000, block_size=9):
        super().__init__(width, height, core_size)
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._screen.fill(Color.BACKGROUND.value)
        self._ticks = ticks
        self._block_size = block_size

    def clock_tick(self):
        self._clock.tick(self._ticks)

    def draw_rect_with_border(self, x, y, width, height, color, border=1, border_color=(0, 0, 0)):
        back = pygame.Rect(x, y, width, height)
        front = pygame.Rect(x + border, y + border, width - border, height - border)
        pygame.draw.rect(self._screen, border_color, back)
        pygame.draw.rect(self._screen, color, front)

    def set_block_color(self, block_number, color):
        x, y = self.get_block_position(block_number)
        x *= self._block_size
        y *= self._block_size
        self.draw_rect_with_border(x, y, self._block_size, self._block_size, color)

    def init_game_screen(self):
        for i in range(self._core_size):
            self.set_block_color(i, Color.GRAY.value)
        pygame.display.flip()
