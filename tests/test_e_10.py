from py_search.uninformed import breadth_first_search, depth_first_search
from py_search.base import Node

from sympy.geometry import Line

from euclidea.e_10 import E10
from euclidea.euclidean_world import EuclideanWorld

goal_world = EuclideanWorld((
    Line(E10.GOAL_POINT, (0, 0)),
    Line(E10.GOAL_POINT, (1, 0)),
))


def test_goal():
    assert E10.GOAL_POINT in goal_world.get_points()


def test_goal_depth_first():
    assert len(list(depth_first_search(E10(goal_world)))) == 1


def test_goal_breadth_first():
    assert len(list(breadth_first_search(E10(goal_world)))) == 1


def test_successors():
    assert E10.INITIAL not in E10().successors(Node(E10.INITIAL))
