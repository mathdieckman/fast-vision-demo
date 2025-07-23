#!/usr/bin/env python
# TODO: fix issue #1 with case when obstacles are triangles and two
#  top-vertices of obstacles and origin are placed in-line horizontally -
#  the top vertex of closer triangle is omitted and an obstacle is cut.

import math
from typing import Tuple, Sequence, Optional, List


EPSILON = 0.05

degrees = math.degrees
hypotenuse = math.hypot


def distance(coord_a: Tuple, coord_b: Tuple) -> float:
    """
    Calculate distance between two points in 2D space.

    :param coord_a: Tuple -- (x, y) coords of first point
    :param coord_b: Tuple -- (x, y) coords of second p
    :return: float -- 2-dimensional distance between segment
    """
    return hypotenuse(coord_b[0] - coord_a[0], coord_b[1] - coord_a[1])


def calculate_vector_2d(angle: float, scalar: float) -> Tuple[float, float]:
    """

    Calculate x and y parts of the current vector.

    :param angle: float -- angle of the vector
    :param scalar: float -- scalar value of the vector (e.g. speed)
    :return: Tuple -- x and y parts of the vector in format: (float, float)
    """
    radians = math.radians(angle)
    change_y = math.cos(radians)
    change_x = math.sin(radians)
    return change_x * scalar, change_y * scalar


def calculate_angle(start: Tuple, end: Tuple) -> float:
    """
    Calculate angle in direction from 'start' to the 'end' point in degrees.

    :param start: Tuple[float, float] -- start point coordinates (x, y)
    :param end: Tuple[float, float] -- end point coordinates (x, y)
    :return: float -- degrees in range 0-360.
    """
    radians = -math.atan2(end[0] - start[0], end[1] - start[1])
    return degrees(radians) % 360


def move_along_vector(start: Tuple[float, float],
                      velocity: float,
                      target: Optional[Tuple[float, float]] = None,
                      angle: Optional[float] = None) -> Tuple[float, float]:
    """
    Create movement vector starting at 'start' point angled in direction of
    'target' point with scalar velocity 'velocity'. Optionally, instead of
    'target' position, you can pass starting 'angle' of the vector.

    Use 'target' position only, when you now the point and do not know the
    angle between two segment, but want quickly calculate position of the
    another point lying on the line connecting two, known segment.

    :param start: Tuple[float, float] -- point from vector starts
    :param target: Optional[Tuple[float, float] -- target the vector 'looks at'
    :param velocity: float -- scalar length of the vector
    :param angle: Optional[float] -- angle of the vector direction
    :return: Tuple[float, float] -- (optional)position of the vector end
    """
    p1 = (start[0], start[1])
    if target:
        p2 = (target[0], target[1])
        # rad = -math.atan2(p2[0] - p1[0], p2[1] - p1[1])
        # angle = degrees(rad) % 360
        angle = calculate_angle(p1, p2)
    if target is None and angle is None:
        raise ValueError("You MUST pass target position or vector angle!")

    v = calculate_vector_2d(angle, velocity)

    return p1[0] + v[0], p1[1] + v[1]


def ccw(points_list: Sequence[Tuple[float, float]]) -> bool:
    """
    Check if sequence of points is oriented in clockwise or counterclockwise
    order.
    """
    a, b, c = points_list[0], points_list[1], points_list[2]
    val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    return val > 0


def are_points_in_line(a: Tuple[float, float],
                       b: Tuple[float, float],
                       c: Tuple[float, float]) -> bool:
    return -EPSILON < (distance(a, c) + distance(c, b) - distance(a, b)) < EPSILON

# create polygon


def regular_polygon(x: float, y: float, edge_ln: float, edge_num: int) -> List:
    """Produce obstacle (polygon) of any size and number
    of vertices."""
    poly = []
    for k in range(edge_num):
        angle = (k - 1) * (360 / edge_num)
        offset = 180 / edge_num
        point = move_along_vector((x, y), edge_ln,
                                  angle=angle - offset)
        poly.append(point)
    return poly

# if __name__=="__main__":
    # from collections import deque
    # inters = deque([])
    # w = WildLight(2,2,(3,4),[[[1,2],[4,6]]])
    # print(w.interp_polar(np.sqrt(2),np.pi*3/4,np.sqrt(2),-np.pi*3/4, np.pi))
    # # a = WildLight.screen_borders_to_corners()

    # # b = WildLight.obstacles_to_wall_points([[[1,3],[1,1],[0,1]],[[2,4],[1.5,1],[2,1]]])

    # # data = np.concatenate([a, b])
    # a = np.zeros((2,4))

    # print(WildLight.shift_rel(a,4,1))

    # z = np.zeros((3,4)) + 6

    # w = WildLight(3,4,(2,3,4),[[[44,33],[4,44],[66,33]]])
    # # w.to_polar(z)
    # w.update_visible_polygon()
    # w.update_visible_polygon()
    # w.update_visible_polygon()

    # print(w.light_polygon)
