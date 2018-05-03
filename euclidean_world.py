import itertools as it
import logging

from sympy.geometry import Point, Line
from sympy.geometry.ellipse import Circle
from sympy.geometry.util import intersection
from sympy.geometry.entity import GeometryEntity

logger = logging.getLogger(None if __name__ == '__main__' else __name__)


class EuclideanWorld:
    def __init__(self, entities=(), normalise_lines=True, points=None):
        self.entities = frozenset(
            self.normalise_line(e)
            if normalise_lines and isinstance(e, Line)
            else e
            for e in entities
        )
        for entity in entities:
            self.type_check(entity)
        self.points = points

    @staticmethod
    def type_check(entity):
        if not isinstance(entity, GeometryEntity):
            raise TypeError(f"All elements of {self.__class__.__name__}"
                            " must be an instance of GeometryEntity")

    def __repr__(self):
        return f"{self.__class__.__name__}({set(self.entities)!r})"

    def __hash__(self):
        return hash(self.entities) + 1

    def __eq__(self, other):
        return isinstance(other, EuclideanWorld) \
            and self.entities == other.entities

    def __lt__(self, other):
        return self.entities < other.entities \
            if isinstance(other, EuclideanWorld) \
            else NotImplemented

    def __gt__(self, other):
        return self.entities > other.entities \
            if isinstance(other, EuclideanWorld) \
            else NotImplemented

    def __le__(self, other):
        return self.entities <= other.entities \
            if isinstance(other, EuclideanWorld) \
            else NotImplemented

    def __ge__(self, other):
        return self.entities >= other.entities \
            if isinstance(other, EuclideanWorld) \
            else NotImplemented

    @staticmethod
    def normalise_line(line):
        """Define a line using points on (0, _) and (1, _)"""
        logger.debug(f"Normalizing {line}")
        if line.p1.x == 0 and line.p2.x == 1:
            # Already normalised
            return line
        if line.p1.x == line.p2.x:
            # Parallel to normalisation lines
            if line.p1.y == 0 and line.p2.y == 1:
                return line
            else:
                return Line((line.p1.x, 0), (line.p1.x, 1))
        # Normalise
        # Not using `else` to catch all uncovered cases of above if-else tree
        return Line(
            Line((0, 0), (0, 1)).intersection(line)[0],
            Line((1, 0), (1, 1)).intersection(line)[0]
        )

    def get_points(self):
        """Get all "interesting" points in the current world"""
        if self.points is None:
            self.points = set(
                it.chain(
                    (
                        e
                        for comb in it.combinations(self.entities, 2)
                        for e in intersection(*comb)
                        if isinstance(e, Point)
                    ),
                    *(
                        e.vertices
                        for e in self.entities
                        if hasattr(e, 'vertices')
                    )
                )
            )
        return self.points

    def add_entity(self, entity):
        """Create a new EuclideanWorld with one additional entity"""
        self.type_check(entity)
        if isinstance(entity, Line):
            entity = self.normalise_line(entity)
        return EuclideanWorld(
            self.entities | {entity},
            False,
            self.get_points().union(
                i
                for e in self.entities
                for i in intersection(entity, e)
                if isinstance(i, Point)
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

    @staticmethod
    def all_lines(points):
        """
        Find all line the can be made using the given points
        """
        return it.starmap(Line, it.combinations(points, 2))
