#!/usr/bin/env python
import pygame.freetype
from constants import (BATTLEFIED_W, BATTLEFIELD_H)

from elems.buttons import (Button, ClampedValue, CheckButton)

pygame.init()
draw = pygame.draw
FONT = pygame.freetype.SysFont("Garamond", 20)
draw_text = FONT.render_to


class OptionsScreen:
    # noinspection PyTypeChecker

    def __init__(self, app):
        self.app = app
        self.options = []
        self.on_options_screen = True
        self.create_interactable_options(app.window)

    def subloop(self, window):
        pass

    def run_application(self):
        self.app.on_options_screen = False
        self.app.on_simulation = True

    def change_edges_count(self):
        self.app.obstacle_edges = self.options[1].value

    def change_edge_size(self):
        self.app.obstacle_edge_size = self.options[2].value

    def toggle_rays(self):
        self.app.show_rays = self.options[3].value

    def toggle_colors(self):
        self.random_colors = self.options[4].value

    def create_interactable_options(self, window):
        p = (BATTLEFIELD_H / 2, BATTLEFIED_W / 2)  # basic position to override
        positions = [(p[0] + 300, p[1]), (p[0], p[1] - 100),
                     (p[0], p[1] - 200),
                     (p[0], p[1] - 300), (p[0], p[1] - 400)]
        types = [Button, ClampedValue, ClampedValue, CheckButton, CheckButton]
        functions = [self.run_application, self.change_edges_count,
                     self.change_edge_size, self.toggle_rays,
                     self.toggle_colors]
        ranges = [None, (3, 20, 1), (25, 200, 25), None, None]
        values = ["Run", 5, 100, self.app.show_rays, self.app.random_colors]
        labels = [None, "Edges:", "Size:", "Show rays?", "Random colors?"]

        for i, position in enumerate(positions):
            if types[i] == ClampedValue:
                _min, _max, step = ranges[i]
                b = ClampedValue(window, *position, 25, 25, values[i], _min,
                                 _max,
                                 step, functions[i], labels[i])
            elif types[i] == CheckButton:
                b = CheckButton(window, *position, 15, 15, values[i],
                                functions[i],
                                labels[i])
            else:
                b = Button(window, *position, 25, 25, values[i], functions[i])
            self.options.append(b)
