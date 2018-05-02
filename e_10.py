import itertools as it

from py_search.base import Problem

from sympy.geometry import Polygon, Line, Point

from .euclidean_world import EuclideanWorld

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

# http://py-search.readthedocs.io/en/latest/py_search.html#py_search.base.Problem
class E10(Problem):
    def __init__(self, initial=None, *args, **kwargs):
        if initial is None:
            initial = EuclideanWorld([Polygon((0, 0), (8, 0), (8, 8), (0, 8))])
        super(E10, self).__init__(initial, *args, **kwargs)

    @staticmethod
    def goal_test(world):
        return Point(4, 3) in world.get_points()

    @staticmethod
    def successors(world):
        nentities = len(world.entities)
        if nentities <= 3:
            # Circles
            points = world.get_points()
            !! WRONG return world.all_circles(points)
        elif nentities <= 5:
            # Lines
            return (
                EuclideanWorld(world.entities | {line})
                for line in it.starmap(
                    Line, it.combinations(world.get_points(), 2)
                )
                if line not in world.entities
            )
        else:
            return ()
