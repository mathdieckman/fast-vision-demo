
from pygame import surface
from constants import (BATTLEFIELD_H, BATTLEFIED_W, GREYS_COUNT,
                       WHITE, GREEN, GREY, RED, DARK)
from mathfuncs.geometry import move_along_vector
from effects.light import WildLight
import random
import pygame
import time
from typing import Tuple, List

get_time = time.perf_counter
draw = pygame.draw
draw_line = draw.line
draw_circle = draw.circle
# draw_textured_poly = pygame.gfxdraw.textured_polygon

draw_polygon = draw.polygon
randint = random.randint

PIECE_RADIUS = 50


class Circle_Dude:
    def __init__(self, window, x: float, y: float, r: float, app,
                 text: str = "", function: callable = None, obstacles=None):

        self.x = x
        self.y = y
        self.r = r
        self.app = app
        self.text = text
        self.window = window
        self.function = function
        self.seen = False
        self.active = False
        self.grabbed = False
        # to draw rays from origin to eah obstacle-corner:
        self.show_rays = True
        # number of origins from where FOV/light polygon will be drawn. Raising this
        # variable will get very costly fast!
        self.lights_count = GREYS_COUNT
        self.random_colors = False
        self.lights = self.create_lights(obstacles)
        self.image = surface.Surface([r, r])
        self.image.fill(GREEN)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def on_mouse_motion(self, x: float, y: float, grabbed=None):
        if self.grabbed:
            self.move_to(x, y)
            self.update_lights()

    def update_lights(self):
        for light in self.lights:
            light.update_visible_polygon()

    def get_light_color(self, random_colors=False) -> Tuple[float, float, float]:
        if random_colors:
            return randint(0, 255), randint(0, 255), randint(0, 255)
        else:
            return GREY

    def get_light_position(self, i: int, x: float, y: float) -> Tuple[float, float]:
        if not i:
            point = (x, y)
        else:
            angle = i * (360 // self.lights_count)
            point = move_along_vector((x, y), self.r, angle=angle)
        return point

    def create_lights(self, obstacles: List) -> List:
        lights: List = []
        x, y = BATTLEFIED_W // 2, BATTLEFIELD_H // 2
        for i in range(self.lights_count):
            color = self.get_light_color(WHITE)
            point = self.get_light_position(i, x, y)
            light = WildLight(*point, color, obstacles,
                              pygame.Surface((BATTLEFIED_W, BATTLEFIELD_H)))
            lights.append(light)
        return lights

    @staticmethod
    def create_points_list(x, y, h, w):
        points = [(x - w, y - h), (x + w, y - h),
                  (x + w, y + h), (x - w, y + h)]
        return points

    def draw(self):
        color = None
        if self.active:
            color = GREEN
        elif self.seen:
            color = RED
        else:
            color = WHITE

        for light in self.lights:
            light.s.fill(DARK)
            polygon = light.light_polygon
            if len(polygon) > 2:
                draw_polygon(light.s, light.color, polygon)
                # x, y = light.origin

            # if self.show_rays:
            #     for i, r in enumerate(polygon):
            #         color = WHITE if i else RED
            #         draw_line(window, color, (x, y), (r[0], r[1]))

        self.window.blits(
            [(light.s, (0, 0), None, pygame.BLEND_ALPHA_SDL2) for light in self.lights])
        draw.circle(self.window, color, (self.x, self.y), self.r, width=0)

        # for light in self.lights:
        #     draw_circle(self.window, BLACK, (int(light.origin[0]), int(light.origin[1])), 5)

    def mouse_over(self, x, y):
        return abs(self.x - x) <= self.r and abs(self.y - y) <= self.r

    def move_to(self, x, y):
        if self.grabbed:
            self.x, self.y = x, y
            if len(self.lights) >= 1:
                for i, light in enumerate(self.lights):
                    angle = i * (360 // (GREYS_COUNT-1))
                    point = None
                    point = move_along_vector((int(x), int(y)), self.r,
                                              angle=angle)
                    light.move_to(point[0], point[1])

    def on_click(self):
        self.grabbed = not self.grabbed
        if not self.grabbed:
            for light in self.lights:
                light.light_polygon = []
