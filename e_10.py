#! /usr/bin/env python3
import logging

from py_search.base import Problem, Node

from sympy.geometry import Polygon, Point

try:
    from euclidean_world import EuclideanWorld
except ImportError:
    try:
        from .euclidean_world import EuclideanWorld
    except ImportError:
        from euclidea.euclidean_world import EuclideanWorld

logger = logging.getLogger(None if __name__ == '__main__' else __name__)

# The goal is to find a circle that is tangent to a side of a given square and
# goes through the (two) vertices of the opposite side.

# This is possible using only 6 basic Euclidean constructions, the hint says:
#   1. Circle
#   2. Circle
#   3. Line
#   4. Line
#   5. Line
#   6. Circle   (This being the circle needed)

# One can draw the needed circle iff the centre is known, because the radius is
# easily defined using one of the vertices it should intersect.

# After being at this problem, I claim the centre `p` is at `Point(4, 3)`, if
# the given square is `Polygon((0, 0), (8, 0), (8, 8), (0, 8))`.

# The algorithm to find `p` should do the following:
#  - if the number of constructions done at a node is ge 5, it should not return
#    successors
#  - I must be able to find all "points" in the current construction:
#       i.e. all intersections of all objects. (I assume the solution can be
#       found using only those points.)
#  - I should create the right object using two of those points


class E10(Problem):
    # FACTOR = 2**5 * 3 ** 5 * 5 ** 5 * 7 ** 5 * 13 ** 5
    # FACTOR = float(1)
    FACTOR = 1
    THREE = 3 * FACTOR
    FOUR = 4 * FACTOR
    EIGHT = FOUR * 2

    INITIAL = EuclideanWorld([Polygon(
        (0, 0),
        (EIGHT, 0),
        (EIGHT, EIGHT),
        (0, EIGHT)
    )])
    GOAL_POINT = Point(FOUR, THREE)

    def __init__(self, initial=None, goal=None, *args, **kwargs):
        if initial is None:
            initial = self.INITIAL
        super(E10, self).__init__(initial, None, *args, **kwargs)

    def goal_test(self, current_node, goal_node):
        return self.GOAL_POINT in current_node.state.get_points()

    @staticmethod
    def successors(node):
        logger.debug(f"getting successors for {node}")
        world = node.state
        nentities = len(world.entities)
        if nentities <= 3:
            logger.debug("Circles")
            # Circles
            for circle in world.all_circles(world.get_points()):
                if circle not in world.entities:
                    yield Node(world.add_entity(circle))
        elif nentities <= 5:
            logger.debug("Lines")
            # Lines
            for line in world.all_lines(world.get_points()):
                if line not in world.entities:
                    try:
                        yield Node(world.add_entity(line))
                    except RuntimeError:
                        logger.warn(f"Couldn't add {line}")
        else:
            logger.debug("Nothing!")
            return


if __name__ == '__main__':
    from py_search.uninformed import depth_first_search
    logging.basicConfig(level="DEBUG")
    print(next(depth_first_search(E10())))
