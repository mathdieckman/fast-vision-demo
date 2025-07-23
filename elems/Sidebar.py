from constants import *
from elems.buttons import (Button, ClampedValue)

class Phase:
    pass

class Scene:
    pass



class Sidebar:
    # noinspection PyTypeChecker

    def __init__(self, app):
        self.app = app
        self.options = []

    def draw(self):
        for op in self.options():
            op.draw()

    def create_interactable_options(self, window):
        p = (BATTLEFIED_W, BATTLEFIELD_H)  # basic position to override

        dbr_w = SIDEBAR_W//6

        # self.options.append(ClampedValue(window, *position, 25, 25, values[i], _min,
        #                          _max,
        #                          step, None, labels[i]))
        
        # self.options.append(ClampedValue(window, *(p[0], p[1] - BATTLEFIELD_H // 4), 25, 25, values[i], _min,
        #                          _max,
        #                          step, None, labels[i]))
        

        self.options.append(
            Button(window, 
                   p[0] + 3*dbr_w//2, p[1] * 3//4, dbr_w//2, dbr_w, 
                   "Move",None))

        self.options.append(
            Button(window, 
                   p[0] + 8*dbr_w//2, p[1]* 3//4, dbr_w//2, dbr_w, 
                   "Shoot",None))
        
        self.options.append(
            ClampedValue(window, 
                         p[0]+ 8*dbr_w//2, p[1] - BATTLEFIELD_H // 2, 
                         25, 25, 
                         5,
                         3, 20, 1,
                         None, "Size:"))

        # positions = [(p[0] + 300, p[1]),
        #              (p[0], p[1] - BATTLEFIELD_H // 4),
        #              (p[0], p[1] - BATTLEFIELD_H // 2),
        #              (p[0], p[1] - (BATTLEFIELD_H * 3) // 4),]
        # types = [Button, ClampedValue, ClampedValue, CheckButton]
        # ranges = [None, (3, 20, 1), (25, 200, 25), None]
        # values = ["Run", 5, 100, self.app.show_rays]
        # labels = [None, "Edges:", "Size:", "Show rays?"]

        # for i, position in enumerate(positions):
            # if types[i] == ClampedValue:
            #     _min, _max, step = ranges[i]
            #     b = ClampedValue(window, *position, 25, 25, values[i], _min,
            #                      _max,
            #                      step, None, labels[i])
            # elif types[i] == CheckButton:
            #     b = CheckButton(window, *position, 15, 15, values[i],
            #                     None,
            #                     labels[i])
            # else:
            #     b = Button(window, *position, 25, 25, values[i], None)
            # self.options.append(b)
