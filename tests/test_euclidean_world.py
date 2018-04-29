from hypothesis import given, settings
from hypothesis.strategies import builds, integers, composite, assume

from sympy.geometry import Point, Line, RegularPolygon
from sympy.geometry.util import intersection

from euclidea.euclidean_world import EuclideanWorld


def points():
    return builds(
        Point,
        integers(min_value=-100, max_value=100),
        integers(min_value=-100, max_value=100)
    )


def regular_polygons():
    return builds(
        RegularPolygon,
        points(),
        integers(min_value=1, max_value=100),
        integers(min_value=3, max_value=100)
    )


@composite
def lines(draw):
    x = draw(points())
    y = draw(points())
    assume(x != y)
    return Line(x, y)


@given(lines(), lines())
def test_points_from_lines(l1, l2):
    if l1.is_similar(l2) or l1.is_parallel(l2):
        assert EuclideanWorld([l1, l2]).get_points() == set()
    else:
        assert EuclideanWorld([l1, l2]).get_points() == set(intersection(l1, l2))


@given(lines())
def test_points_from_single_line(l1):
    assert EuclideanWorld([l1]).get_points() == set()


@settings(max_examples=10)
@given(regular_polygons())
def test_points_from_polygon(rp):
    """A polygon should have its vertices as points"""
    assert EuclideanWorld([rp]).get_points() == set(rp.vertices)


@settings(max_examples=1, max_shrinks=1)
@given(points(), regular_polygons())
def test_points_from_polygon_and_line(p, rp):
    """A Line through the centre of a polygon should have two intersections"""
    centre = rp.args[0]
    assume(p != centre)
    line = Line(p, centre)
    assert len(EuclideanWorld([rp, line]).get_points()) == 2 + rp.args[2]
