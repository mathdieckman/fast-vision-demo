from constants import (BATTLEFIED_W, BATTLEFIELD_H, SIDEBAR_W)
from elems.buttons import (Button, ClampedValue)
from elems.units import Circle_Dude
from maps.demo import DemoMap


class Phase:
    pass


class DemoScene:

    def __init__(self, app):
        obstacle_edges = 20
        obstacle_edge_size = 20
        app.map = DemoMap(obstacle_edge_size, obstacle_edges)
        app.walls = app.map.create_obstacles()
        dude1 = Circle_Dude(app.window, 30, 20, 10, app,
                            obstacles=app.map.obstacles)
        dude2 = Circle_Dude(app.window, 30, 10, 10, app,
                            obstacles=app.map.obstacles)
        app.sb = Sidebar(app)
        app.sb.create_interactable_options(app.window)

        app.clickables.append(dude1)
        app.clickables.append(dude2)
        app.clickables.extend(app.sb.options)

        app.hoverables.append(dude1)
        app.hoverables.append(dude2)
        app.hoverables.extend(app.sb.options)

        app.drawables.append(dude1)
        app.drawables.append(dude2)
        app.drawables.extend(app.sb.options)


class Sidebar:
    # noinspection PyTypeChecker

    def __init__(self, app):
        self.app = app
        self.options = []

    def create_interactable_options(self, window):
        p = (BATTLEFIED_W, BATTLEFIELD_H)  # basic position to override

        dbr_w = SIDEBAR_W//6

        self.options.append(
            Button(window,
                   p[0] + 3*dbr_w//2, p[1] * 3//4, dbr_w//2, dbr_w,
                   "Move", None))

        self.options.append(
            Button(window,
                   p[0] + 8*dbr_w//2, p[1] * 3//4, dbr_w//2, dbr_w,
                   "Shoot", None))

        self.options.append(
            ClampedValue(window,
                         p[0] + 8*dbr_w//2, p[1] - BATTLEFIELD_H // 2,
                         25, 25,
                         5,
                         3, 20, 1,
                         None, "Size:"))
