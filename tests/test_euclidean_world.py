from pytest import raises

from hypothesis import given, settings
from hypothesis.strategies import integers, sets
from hypothesis.strategies import builds, composite, assume

from sympy.geometry import Point, Line, RegularPolygon
from sympy.geometry.util import intersection
from sympy.geometry.ellipse import Circle

from euclidea.euclidean_world import EuclideanWorld


def points():
    x = integers(min_value=-100, max_value=100)
    y = integers(min_value=-100, max_value=100)
    return builds(Point, x, y)


@composite
def regular_polygons(draw, not_centre=None):
    centre = points()
    if not_centre:
        centre = centre.filter(centre.__ne__)

    return RegularPolygon(
        draw(centre),
        draw(integers(min_value=1, max_value=100)),
        draw(integers(min_value=3, max_value=6))
    )


@composite
def regular_polygon_and_point_pairs(draw):
    """
    Generate a point and a regular polygon who's centre is different from the
    generated point
    """
    p = draw(points())
    rp = draw(regular_polygons(p))
    return (p, rp)


@composite
def lines(draw):
    p = points()
    x = draw(p)
    y = draw(p)
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
@given(regular_polygon_and_point_pairs())
def test_points_from_polygon_and_line(pair):
    """A Line through the centre of a polygon should have two intersections"""
    p, rp = pair
    centre = rp.args[0]
    assume(p != centre)
    line = Line(p, centre)
    assert len(EuclideanWorld([rp, line]).get_points()) == 2 + rp.args[2]


@given(points())
def test_circles_one_point(p):
    """
    Check whether `all_circles` yields all expected circles with one point
    """
    empty = EuclideanWorld.all_circles([p])
    with raises(StopIteration):
        next(empty)


@given(points(), points())
def test_all_circles_two_points(p1, p2):
    """
    Check whether `all_circles` yields all expected circles with two points
    """
    assume(p1 != p2)
    two_circles = EuclideanWorld.all_circles([p1, p2])
    assert len(two_circles) == 2
    r = p1.distance(p2)
    assert Circle(p1, r) in two_circles
    assert Circle(p2, r) in two_circles


@given(points(), points(), points())
def test_all_circles_two_points(p1, p2, p3):
    """
    Check whether `all_circles` yields all expected circles with three points
    """
    assume(p1 != p2)
    assume(p2 != p3)
    assume(p3 != p1)
    two_circles = list(EuclideanWorld.all_circles([p1, p2, p3]))
    assert len(two_circles) <= 6
    assert len(two_circles) >= 3
    assert Circle(p1, p1.distance(p2)) in two_circles
    assert Circle(p1, p1.distance(p3)) in two_circles
    assert Circle(p2, p2.distance(p1)) in two_circles
    assert Circle(p2, p2.distance(p3)) in two_circles
    assert Circle(p3, p3.distance(p1)) in two_circles
    assert Circle(p3, p3.distance(p2)) in two_circles


@given(sets(points()))
def test_all_circles_count(points):
    """Check whether `all_circles` yields the expected number of circles"""
    assume(len(points) > 1)
    circles = list(EuclideanWorld.all_circles(points))
    assert len(circles) <= len(points) * (len(points) - 1)
    assert len(circles) >= len(points)
