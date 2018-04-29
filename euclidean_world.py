import itertools as it

from sympy.geometry import Point
from sympy.geometry.ellipse import Cicle
from sympy.geometry.util import intersection


class EuclideanWorld:
    def __init__(self, entities):
        self.entities = set(entities)

    def get_points(self):
        """Get all "interesting" points in the current world"""
        return set(
            it.chain(
                *(
                    (e for e in intersection(*comb) if isinstance(e, Point))
                    for comb in it.combinations(self.entities, 2)
                ),
                *(e.vertices for e in self.entities if hasattr(e, 'vertices'))
            )
        )

    @staticmethod
    def all_circles(points):
        """
        Find all circles the can be made using the given points as centre and "radius"
        """
        for centre in points:
            radii = set(
                centre.distance(other)
                for other in points
                if other != centre
            )
            for radius in radii:
                yield Circle(centre, radius)
