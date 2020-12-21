from abc import abstractmethod

import pygame

from src.enum.event import CoreEvent
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

    def get_block_position(self, block_number):
        y = block_number // self._blocks_x
        x = block_number % self._blocks_x
        return x, y

    @abstractmethod
    def init_game_screen(self):
        pass

    @abstractmethod
    def set_block_color(self, block_number, color, event):
        events_method = {
            CoreEvent.READ: self._set_block_read,
            CoreEvent.WRITE: self._set_block_written,
            CoreEvent.EXECUTE: self._set_block_executed,
        }
        events_method[event](block_number, color)

    @abstractmethod
    def _set_block_read(self, block_number, color):
        pass

    @abstractmethod
    def _set_block_written(self, block_number, color):
        pass

    @abstractmethod
    def _set_block_executed(self, block_number, color):
        pass


class PyGameGUI(GUI):
    def __init__(self, width, height, ticks=250, core_size=8000, block_size=10):
        super().__init__(width, height, core_size)
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._screen.fill(Color.BACKGROUND.value)
        self._ticks = ticks
        self._block_size = block_size

    def clock_tick(self):
        self._clock.tick(self._ticks)

    def _draw_rect_with_border(self, x, y, width, height, color, border=1, border_color=(0, 0, 0)):
        back = pygame.Rect(x, y, width, height)
        front = pygame.Rect(x + border, y + border, width - border, height - border)
        pygame.draw.rect(self._screen, border_color, back)
        pygame.draw.rect(self._screen, color, front)

    def _draw_circle_with_border(self, x, y, width, height, color, border=1, border_color=(0, 0, 0)):
        self._draw_rect_with_border(x, y, width, height, Color.GRAY.value)
        pygame.draw.circle(self._screen, color, (x + 4, y + 4), 3)

    def _draw_x(self, x, y, width, height, color, border=1, border_color=(0, 0, 0)):
        self._draw_rect_with_border(x, y, width, height, Color.GRAY.value)
        pygame.draw.line(self._screen, color, (x + border, y + border),
                         (x + self._block_size - border, y + self._block_size - border), width=3)
        pygame.draw.line(self._screen, color, (x + self._block_size - border, y + border),
                         (x + border, y + self._block_size - border), width=3)

    def _get_position_in_pixels(self, block_number):
        x, y = self.get_block_position(block_number)
        x *= self._block_size
        y *= self._block_size
        return x, y

    def _set_block_read(self, block_number, color):
        x, y = self._get_position_in_pixels(block_number)
        # self._draw_circle_with_border(x, y, self._block_size, self._block_size, color)

    def _set_block_written(self, block_number, color):
        x, y = self._get_position_in_pixels(block_number)
        self._draw_x(x, y, self._block_size, self._block_size, color)

    def _set_block_executed(self, block_number, color):
        x, y = self._get_position_in_pixels(block_number)
        self._draw_rect_with_border(x, y, self._block_size, self._block_size, color)

    def init_game_screen(self):
        for i in range(self._core_size):
            self.set_block_color(i, Color.GRAY.value, CoreEvent.EXECUTE)
        pygame.display.flip()
