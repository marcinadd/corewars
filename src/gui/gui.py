import math
from abc import abstractmethod

import pygame

from src.enum.event import CoreEvent
from src.gui.colors import Color
from src.gui.strings import STRINGS

BLOCKS_X = 100
FONT_LOCATION = "font/font.ttf"


def divide_blocks(core_size):
    return BLOCKS_X, math.ceil(core_size // BLOCKS_X)


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

    def init_game_screen(self):
        self._init_core_view()
        self._init_info_view()

    @abstractmethod
    def _init_core_view(self):
        pass

    @abstractmethod
    def _init_info_view(self):
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

    @abstractmethod
    def print_round_text(self, round):
        pass

    @abstractmethod
    def clock_tick(self):
        pass


class PyGameGUI(GUI):
    def __init__(self, width, height, core_size, ticks=250, block_size=10):
        super().__init__(width, height, core_size)
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._screen.fill(Color.BACKGROUND.value)
        self._ticks = ticks
        self._block_size = block_size
        self._width = width

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

    def _init_core_view(self):
        for i in range(self._core_size):
            self.set_block_color(i, Color.GRAY.value, CoreEvent.EXECUTE)
        pygame.display.flip()

    def _init_info_view(self):
        self.print_round_text(0)

    def _get_start_info_position(self):
        return BLOCKS_X * self._block_size

    def print_round_text(self, round_num):
        font = pygame.font.Font(FONT_LOCATION, 16)
        text = font.render(f'{STRINGS["ROUND"]} {round_num}', True, Color.TEXT_COLOR.value)
        text_rect = text.get_rect()
        info_block_start_position = self._get_start_info_position()
        position_x = (self._width - info_block_start_position) // 2 + info_block_start_position
        text_rect.center = (position_x, 20)
        self._screen.blit(text, text_rect)
        pygame.display.update()
