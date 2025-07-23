
import pygame.freetype
from constants import BLACK, WHITE, GREY, GREEN

from mathfuncs.geometry import ccw
import math

pygame.init()
draw = pygame.draw
FONT = pygame.freetype.SysFont("Garamond", 20)
draw_text = FONT.render_to


class Button:

    def __init__(self, window, x: float, y: float, h: float, w: float,
                 text: str = "", function: callable = None):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.text = text
        self.points = self.create_points_list(x, y, h, w)
        self.window = window
        self.function = function
        self.active = False

    @staticmethod
    def create_points_list(x, y, h, w):
        points = [(x - w, y - h), (x + w, y - h),
                  (x + w, y + h), (x - w, y + h)]
        return points

    def draw(self):
        color = GREEN if self.active else WHITE
        draw.polygon(self.window, color, self.points)
        if self.text:
            draw_text(self.window, (self.x - 20, self.y - 10), self.text,
                      BLACK)

    def mouse_over(self, x, y):
        return abs(self.x - x) <= self.w and abs(self.y - y) <= self.h

    def on_click(self):
        try:
            self.function()
        except TypeError:
            pass

    def on_mouse_motion(self, x, y, grabbed=None):
        pass


class ClampedValue(Button):
    """
    A switch with value and two buttons: one to increase the value and other to
    decrease it.
    """

    def __init__(self, window, x: float, y: float, h: float, w: float,
                 value: int, min: int = 0, max: int = math.inf, step: int = 1,
                 function: callable = None, label: str = "ClampedValue"):
        super().__init__(window, x, y, h, w, function=function)
        self.value = value
        self.min = min
        self.max = max
        self.step = step
        self.window = window
        self.points = self.create_points_lists(x, y, h, w)
        self.active_button = None
        self.label = label

    @staticmethod
    def create_points_lists(x, y, h, w):
        # counter:
        ww, www = 2 * w, 3 * w
        switch = [(x - w, y - h), (x + w, y - h), (x + w, y + h),
                  (x - w, y + h)]
        # increment button:
        plus_btn = [(x + w, y - h), (x + ww, y - h), (x + www, y),
                    (x + ww, y + h), (x + w, y + h)]
        # decrement button:
        min_btn = [(x - w, y - h), (x - w, y + h), (x - ww, y + h),
                   (x - www, y), (x - ww, y - h), ]
        return [switch, plus_btn, min_btn]

    def draw(self):
        # elements:
        for i, element in enumerate(self.points):
            if i:
                color = GREEN if self.active_button == i else GREY
            else:
                color = WHITE
            draw.polygon(self.window, color, element)
        x, y, h, w = self.x, self.y, self.h, self.w
        # value:
        draw_text(self.window, (x - 5, y - 5), str(self.value), BLACK)
        # + and -
        draw_text(self.window, (x + 1.6 * w, y - 5), "+", BLACK)
        draw_text(self.window, (x - 2 * w, y), "-", BLACK)
        # label:
        offset = len(self.label) * 30
        draw_text(self.window, (x - offset, y - 0.5 * w), self.label, WHITE)

    def mouse_over(self, x, y):
        # to check if cursor is pointing at one of the switch-buttons,
        # we just test if cursor position is inside polygon, by checking if
        # all segments are in counter-clockwise order to cursor position:
        for j, element in enumerate(self.points):
            for i, point in enumerate(element):
                if i == len(element) - 1:
                    edge = (point, element[0], (x, y))
                else:
                    edge = (point, element[i + 1], (x, y))
                if ccw(edge):
                    break
            else:
                self.active_button = j
                return True
        self.active_button = None
        return False

    def on_click(self):
        if self.active_button == 1 and self.value < self.max:
            self.value += self.step
        elif self.active_button == 2 and self.value > self.min:
            self.value -= self.step
        super().on_click()


class CheckButton(Button):
    """
    Simple checkbutton storing a single boolean value determining it's state.
    """

    def __init__(self, window, x: float, y: float, h: float, w: float,
                 value: bool = False, function: callable = None,
                 label: str = "Checkbutton"):
        super().__init__(window, x, y, h, w, function=function)
        self.value = value
        self.label = label

    def draw(self):
        super().draw()
        x, y, h, w = self.x, self.y, self.h, self.w
        # tick:
        if self.value:
            tick = [(x - w, y), (x, y + h), (x, y + h), (x + w, y - h)]
            draw.lines(self.window, BLACK, False, tick, 8)
        # label:
        offset = len(self.label) * 14
        draw_text(self.window, (x - offset, y - 0.5 * w), self.label, WHITE)

    def on_click(self):
        self.value = not self.value
        super().on_click()
