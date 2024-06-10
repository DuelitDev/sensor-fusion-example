import math

__all__ = [
    "Vector3"
]


class Vector3:
    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        self._z = value

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
