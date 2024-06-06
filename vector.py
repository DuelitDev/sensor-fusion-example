import math


class Vector3:
    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def z(self) -> float:
        return self._z

    @property
    def magnitude(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    def __init__(self, x: float, y: float, z: float):
        self._x, self._y, self._z = x, y, z

    def normalize(self):
        magnitude = self.magnitude
        if not magnitude:
            return
        self._x /= magnitude
        self._y /= magnitude
        self._z /= magnitude
