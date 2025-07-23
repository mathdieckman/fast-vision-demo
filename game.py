#!/usr/bin/env python
import cProfile
import asyncio
import pstats
# import randomwh
# import time

# from functools import wraps
# from typing import List, Tuple, Optional

import pygame
from constants import (BATTLEFIED_W, SIDEBAR_W,
                       BATTLEFIELD_H, DARK, TITLE, PROFILE)
# import pygame.freetype
# from scenes.options import (OptionsScreen)
# from scenes.fight import (Fight)
# from elems.buttons import Button
from application import Application as App

# from elems.units import Circle_Dude

# FONT = pygame.freetype.SysFont("Garamond", 20)


pygame.init()


def mouse_draw_loop(app):
    window = app.window
    pointed = None  # tracks currently moused over element
    window.fill(DARK)
    on_screen = True

    while on_screen:
        clicked_this_frame = False

        for event in reversed(pygame.event.get()):
            match event.type:
                case pygame.QUIT:
                    pygame.quit()

                case pygame.MOUSEBUTTONDOWN:
                    if clicked_this_frame:
                        continue
                    if event.button == 1:  # mouse left button
                        if pointed is not None:
                            pointed.on_click()
                            break

                case pygame.MOUSEMOTION:
                    x, y = event.pos
                    pointed = None
                    for item in app.hoverables:
                        item.active = item.mouse_over(x, y)
                        if item.active:
                            pointed = item
                        item.on_mouse_motion(x, y)
                    break

        app.draw()
        pygame.display.update()


if __name__ == "__main__":
    window = pygame.display.set_mode((BATTLEFIED_W + SIDEBAR_W, BATTLEFIELD_H))
    pygame.display.set_caption(TITLE)

    application = App(window)

    if PROFILE:
        profiler = cProfile.Profile()
        profiler.enable()

    mouse_draw_loop(application)

    if PROFILE:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats("cumtime")
        stats.print_stats()
