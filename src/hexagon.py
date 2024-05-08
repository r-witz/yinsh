from pygame import Vector2
from math import sqrt

class Hexagon:

    def __init__(self, x: int, y: int, size: int) -> None:
        """
        Initialize a hexagon object with its properties.
        :param x: int, X-coordinate of the center of the hexagon on the pygame.Surface
        :param y: int, Y-coordinate of the center of the hexagon on the pygame.Surface
        :param size: int, Size of the hexagon, used to be displayed on the pygame.Surface
        """
        self.state = "EMPTY" # EMPTY, RING_P1, RING_P2
        self.marker = "EMPTY" # EMPTY, MARKER_P1, MARKER_P2

        self.center = (x, y)
        self.size = size
        self.width = 2*size
        self.height = sqrt(3)*size

        # Positions of the 6 points of the Hexagon, used to be drawn, or calculate if we click inside the Hexagon, with pixel perfect precision.
        self.positions = [
            (x-size, y),
            (x-size/2, y-self.height/2),
            (x+size/2, y-self.height/2),
            (x+size, y),
            (x+size/2, y+self.height/2),
            (x-size/2, y+self.height/2)
        ]

    def contains(self, point: tuple[float, float]) -> bool:
        """
        Check if a point is inside the hexagon.
        :param point: tuple(float, float), Coordinates (x, y) of the point to check.
        :return: bool, True if the point is inside the hexagon, False otherwise.
        """
        x, y = point
        return all(Vector2(x, y).distance_to(Vector2(px, py)) <= self.size*2 for px, py in self.positions)
