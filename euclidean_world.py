import itertools as it

from sympy.geometry import Point
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
