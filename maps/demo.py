
from abc import ABC, abstractmethod
from constants import (BATTLEFIED_W, BATTLEFIELD_H)
from mathfuncs.geometry import regular_polygon
from typing import List


class Map(ABC):
    def __init__(self):
        self.obstacles = None

    @abstractmethod
    def create_obstacles(self) -> List:
        pass


class DemoMap(Map):
    def __init__(self, obstacle_edge_size, obstacle_edges):
        super().__init__()
        self.obstacles = None
        self.obstacle_edge_size = obstacle_edge_size
        self.obstacle_edges = obstacle_edges

    def create_obstacles(self) -> List:
        self.obstacles = []
        size = self.obstacle_edge_size
        for i in range(size * 2, BATTLEFIED_W, size * 3):
            for j in range(size * 2, BATTLEFIELD_H, size * 3):
                obstacle = regular_polygon(
                    i, j, self.obstacle_edge_size, self.obstacle_edges)
                self.obstacles.append(obstacle)

        return self.obstacles


if __name__ == "__main__":
    map = DemoMap(10, 20)
    print(map.create_obstacles())
