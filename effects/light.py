
import math
from typing import List, Tuple

import numpy as np
from collections import deque
from constants import *


show_rays=False
# type of polygon is determined by the number of edges: 3 = triangle,
# 4 = square, 5 = pentagon, 6 = hexagon etc.

class WildLight:
    def __init__(self, x: int, y: int, color: Tuple, obstacles: List, surface, static=0):
        self.inters=deque()

        self.origin = x,y  # position of the light/observer
        self.last = x,y
        self.color = color

        self.border_walls = self.screen_borders_to_corners()
        self.obstacles = obstacles

        self.corners = np.concatenate([self.obstacles_to_wall_points(obstacles),self.border_walls])
        self.light_polygon: List = []

        self.polar = np.zeros_like(self.corners)
        surface.set_alpha(30)
        self.static = static
        self.s = surface

    def move_to(self, x, y):
        self.origin = x, y

    
    @staticmethod
    def screen_borders_to_corners() -> Tuple:
        box = ((0,0),(BATTLEFIED_W, 0), (BATTLEFIED_W,BATTLEFIELD_H), (0, BATTLEFIELD_H))
        walls = np.zeros((8,4))
        for x in range(4):
            for y in range(2):
                walls[x,y] = (1-SHRINK_FACTOR)*box[(x+1)%4][y] + SHRINK_FACTOR*box[x][y]
                walls[x,y+2] = (1-SHRINK_FACTOR)*box[x][y] + SHRINK_FACTOR*box[(x+1)%4][y]

        for x in range(4):
            for y in range(2):
                walls[4+x,y] = (1-SHRINK_FACTOR)*box[x][y] + SHRINK_FACTOR*box[(x+1)%4][y]
                walls[4+x,y+2] = (1-SHRINK_FACTOR)*box[(x+1)%4][y] + SHRINK_FACTOR*box[x][y]
    
        return walls

        
    @staticmethod
    def obstacles_to_wall_points(obstacles: List) -> np.ndarray:
        segs = np.zeros((sum([2*len(ob) for ob in obstacles]), 4))
        i = 0
        for obstacle in obstacles:
            vertex_count = len(obstacle)
            for j in range(vertex_count):
                segs[2*i,0] = (1-SHRINK_FACTOR)*obstacle[j%vertex_count][0] + SHRINK_FACTOR*(obstacle[(j+1)%vertex_count][0])
                segs[2*i,1] = (1-SHRINK_FACTOR)*obstacle[j%vertex_count][1] + SHRINK_FACTOR*(obstacle[(j+1)%vertex_count][1])
                segs[2*i,2] = (1-SHRINK_FACTOR)*obstacle[(j+1)%vertex_count][0] + SHRINK_FACTOR*(obstacle[j%vertex_count][0])
                segs[2*i,3] = (1-SHRINK_FACTOR)*obstacle[(j+1)%vertex_count][1] + SHRINK_FACTOR*(obstacle[j%vertex_count][1])

                segs[2*i+1,0] = (1-SHRINK_FACTOR)*obstacle[(j+1)%vertex_count][0] +  SHRINK_FACTOR*(obstacle[j%vertex_count][0])
                segs[2*i+1,1] = (1-SHRINK_FACTOR)*obstacle[(j+1)%vertex_count][1] + SHRINK_FACTOR*(obstacle[j%vertex_count][1])
                segs[2*i+1,2] = (1-SHRINK_FACTOR)*obstacle[j%vertex_count][0] + SHRINK_FACTOR*(obstacle[(j+1)%vertex_count][0])
                segs[2*i+1,3] = (1-SHRINK_FACTOR)*obstacle[j%vertex_count][1] + SHRINK_FACTOR*(obstacle[(j+1)%vertex_count][1])
                i += 1
        return segs


    @staticmethod
    def shift_rel(arr, x, y):
        return arr - np.array([x,y,x,y])
    
    
    def rel_to_polar(self, arr):
        self.polar[:,0] = np.sqrt(np.square(arr[:,0])+np.square(arr[:,1]))
        self.polar[:,2] = np.sqrt(np.square(arr[:,2])+np.square(arr[:,3]))
        self.polar[:,1] = np.arctan2(arr[:,1],arr[:,0])
        self.polar[:,3] = np.arctan2(arr[:,3],arr[:,2])
        return self.polar

    @staticmethod
    def polar_to_rel(r,theta):
        return r*math.cos(theta), r*math.sin(theta)

    @staticmethod
    def interp_polar(r1,th1,r2,th2,th3):
        ang = th2-th1
        y2 = r2 * math.sin(ang)
        m3 =  math.tan(th3-th1)

        x3=(y2*r1)/(m3*(r2*math.cos(ang)-r1)-y2)
        
        return math.sqrt(1+m3*m3)*abs(x3), th3
    
    def update_visible_polygon(self) -> None:
        # only recalculate if moved
        if self.last == self.origin:
            return
        else:
            self.last = self.origin

        # don't try to draw if close enough to offscreen that rays miss the outer walls
        if (self.origin[0] >= BATTLEFIED_W * (1-SHRINK_FACTOR) or
                self.origin[0] <= BATTLEFIED_W * SHRINK_FACTOR or
                self.origin[1] >= BATTLEFIELD_H * (1-SHRINK_FACTOR) or
                self.origin[1] <= BATTLEFIED_W * SHRINK_FACTOR):
            self.light_polygon = []
            return
        
        self.inters.clear()
        poly = []
        pp = self.rel_to_polar(WildLight.shift_rel(self.corners, self.origin[0], self.origin[1]))
        pp = pp[pp[:, 1].argsort(stable=True)]
        start = []

        # initialize ray-intersection deque
        for x in reversed(range(pp.shape[0])):
            if np.abs(pp[x,1]-pp[x,3])>np.pi:
                if pp[x,1]<=pp[x,3]:
                    start.append((pp[x,0],pp[x,1],pp[x,2],pp[x,3]))

        start.sort(key=lambda x: self.interp_polar(x[2],x[3],
                                                   x[0],x[1],
                                                   np.pi)[0],
                   reverse=True)
        
        begin = self.interp_polar(start[-1][2],start[-1][3],
                                  start[-1][0],start[-1][1],
                                  np.pi)


        last = begin[0], begin[1], start[-1][2], start[-1][3]
        self.inters.extend(start)
        
        # sweep
        for x in reversed(range(pp.shape[0])):
            if (pp[x, 2],pp[x, 3],pp[x, 0],pp[x, 1]) in self.inters:  # if other endpoint of segment has been seen
                self.inters.remove((pp[x, 2],pp[x, 3],pp[x, 0],pp[x, 1]) )    
                if len(self.inters):
                    it = self.inters.pop()    
                    poly.append((last[2],last[3]))
                    poly.append((WildLight.interp_polar(it[0], it[1], it[2], it[3], last[3])))
                    last = it
                    self.inters.append(it)
            else:
                for y in range(len(self.inters)):  # find right place to insert to list of ray intersects
                    if ((not(pp[x,0] < self.inters[y][0] and pp[x,2] < self.inters[y][2])) and 
                            (pp[x,0] > self.interp_polar(self.inters[y][0], self.inters[y][1],
                                                         self.inters[y][2], self.inters[y][3],
                                                         pp[x,1])[0])):
                        self.inters.insert(y,(pp[x, 0], pp[x, 1], pp[x, 2], pp[x, 3]))
                        break
                else:
                        self.inters.append((pp[x, 0], pp[x, 1], pp[x, 2], pp[x, 3]))

                it = self.inters.pop()    
                poly.append((WildLight.interp_polar(last[0], last[1], last[2], last[3], it[1])))
                poly.append((it[0], it[1]))
                last = it
                self.inters.append(it)

        shift = lambda z: (z[0] + self.origin[0], z[1] + self.origin[1])
        self.light_polygon = [shift(WildLight.polar_to_rel(x1,y1)) for x1, y1 in poly]
