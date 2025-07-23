import pygame
from constants import BLACK, DARK
from maps.demo import DemoMap
from elems.units import Circle_Dude
from elems.Sidebar import Sidebar
from scenes.fight import DemoScene


class Application:
    def __init__(self, window):
        self.clickables = []
        self.hoverables = []
        self.drawables = []
        self.walls = []
        self.scenes = []
        self.window = window
        self.scenes = []
        self.scenes.append(DemoScene(self))

    def draw_obstacles(self):
        for obstacle in self.walls:
            pygame.draw.polygon(self.window, BLACK, obstacle)

    def draw(self):
        self.window.fill(DARK)
        for elem in self.drawables:
            elem.draw()

        self.draw_obstacles()
