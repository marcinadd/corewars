import math
from abc import abstractmethod, ABC

import pygame

from src.enum.event import CoreEvent
from src.gui.colors import Color
from src.gui.strings import STRINGS

BLOCKS_X = 100
FONT_LOCATION = "font/font.ttf"


def divide_blocks(core_size):
    return BLOCKS_X, math.ceil(core_size // BLOCKS_X)


class GUI(ABC):
    def __init__(self, width, height, core_size):
        """
        GUI constructor
        :param width: Screen width
        :param height: Screen height
        :param core_size: Core size
        """
        self._width = width
        self._height = height
        self._blocks_x, self._blocks_y = divide_blocks(core_size)
        self._core_size = core_size

    def get_block_position(self, block_number):
        """
        Get block in core position
        :param block_number: Block number to get position
        :return: A tuple with block position (column,row)
        """
        row = block_number // self._blocks_x
        column = block_number % self._blocks_x
        return column, row

    def init_game_screen(self):
        """
        Init game screen: clear core and render game info
        :return:
        """
        self._init_core_view()
        self._init_info_view()

    @abstractmethod
    def _init_core_view(self):
        """
        Print empty core blocks
        """
        pass

    @abstractmethod
    def _init_info_view(self):
        """
        Print info block
        """
        pass

    def set_block_color(self, block_number, color, event):
        """
        Set block with color with style depending on event
        :param block_number: Block to change color
        :param color: New color
        :param event: Event type
        """
        events_method = {
            CoreEvent.READ: self._set_block_read,
            CoreEvent.WRITE: self._set_block_written,
            CoreEvent.EXECUTE: self._set_block_executed,
        }
        events_method[event](block_number, color)

    @abstractmethod
    def _set_block_read(self, block_number, color):
        """
        Set block as read
        :param block_number: Block to set
        :param color: New color
        """
        pass

    @abstractmethod
    def _set_block_written(self, block_number, color):
        """
        Set block as written
        :param block_number: Block to set
        :param color: New color
        """
        pass

    @abstractmethod
    def _set_block_executed(self, block_number, color):
        """
        Set block as executed
        :param block_number: Block to set
        :param color: New color
        """
        pass

    @abstractmethod
    def print_round_text(self, round_num):
        """
        Print text with Round
        :param round_num:
        :return:
        """
        pass

    @abstractmethod
    def print_game_info(self, warriors, cycles):
        """
        Print current game status
        :param warriors: All warriors
        :param cycles:  Current round cycles
        """
        pass

    @abstractmethod
    def clock_tick(self):
        """
        Control game speed depending on GUI implementation
        """
        pass

    @abstractmethod
    def handle_events(self):
        """
        Handle gui events such a window closed, window resized etc.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Handle GUI close
        """
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
        pass

    def _get_start_info_position(self):
        return BLOCKS_X * self._block_size

    def _get_info_x_center(self):
        info_block_start_position = self._get_start_info_position()
        return (self._width - info_block_start_position) // 2

    def print_round_text(self, round_num):
        text = f'{STRINGS["ROUND"]} {round_num}'
        offset_x = self._get_info_x_center()
        offset_y = 20
        self._print_standard_info_text(text, 20, offset_x, offset_y, center=True)
        pygame.display.update()

    def _print_standard_info_text(self, text_str, font_size, offset_x, offset_y, text_color=Color.TEXT_COLOR.value,
                                  center=False):
        font = pygame.font.Font(FONT_LOCATION, font_size)
        text = font.render(text_str, True, text_color, Color.BACKGROUND.value)
        text_rect = text.get_rect()
        info_block_start_x_position = self._get_start_info_position()
        text_position = (offset_x + info_block_start_x_position, offset_y)
        if center:
            text_rect.center = text_position
        else:
            text_rect.topleft = text_position
        self._screen.blit(text, text_rect)

    def _print_warrior_name(self, warrior_number, warrior):
        name = warrior.warrior_info().name()
        offset_x = self._get_info_x_center()
        offset_y = 100 + warrior_number * 100
        self._print_standard_info_text(name, 13, offset_x, offset_y, warrior.color(), center=True)

    def _print_warrior_details(self, warrior_number, warrior):
        offset_x = 10
        offset_y = 110 + warrior_number * 100
        # Print Won-Lost-Tied
        info = warrior.warrior_info()
        wlt = f'W-L-T: {info.wins()}-{info.loses()}-{info.ties()}\t'
        self._print_standard_info_text(wlt, 12, offset_x, offset_y)
        # Print Processes
        offset_y += 15
        processes = f'Processes: {len(warrior.processes()): 4}\t'
        self._print_standard_info_text(processes, 12, offset_x, offset_y)

    def _print_cycles(self, cycles):
        text = f'Cycles: {cycles:5}'
        offset_x = 10
        offset_y = 40
        self._print_standard_info_text(text, 14, offset_x, offset_y)

    def print_game_info(self, warriors, cycles):
        for i, warrior in enumerate(warriors):
            self._print_warrior_name(i, warrior)
            self._print_warrior_details(i, warrior)
            self._print_cycles(cycles)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Simulation aborted!")
                pygame.quit()

    def close(self):
        pygame.quit()


class MockGUI(GUI):
    def __init__(self, core_size):
        super().__init__(0, 0, core_size)

    def _init_core_view(self):
        pass

    def _init_info_view(self):
        pass

    def _set_block_read(self, block_number, color):
        pass

    def _set_block_written(self, block_number, color):
        pass

    def _set_block_executed(self, block_number, color):
        pass

    def print_round_text(self, round_num):
        pass

    def print_game_info(self, warriors, cycles):
        pass

    def clock_tick(self):
        pass

    def handle_events(self):
        pass

    def close(self):
        pass
