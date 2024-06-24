import math

__all__ = [
    "Vector3"
]


class Vector3:
    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = value

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float):
        self._z = value

    @property
    def v(self) -> tuple[float, float, float]:
        return self._x, self._y, self._z

    @v.setter
    def v(self, value: tuple[float, float, float]):
        self._x, self._y, self._z = value

    @property
    def magnitude(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @property
    def normalized(self) -> "Vector3":
        v = Vector3(self._x, self._y, self._z)
        v.normalize()
        return v

    def __init__(self, x: float, y: float, z: float):
        self._x, self._y, self._z = x, y, z

    def __repr__(self) -> str:
        return f"Vector3({self._x}, {self._y}, {self._z})"

    def __add__(self, other: "Vector3 | int | float") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(self._x + other.x,
                           self._y + other.y,
                           self._z + other.z)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(self._x + other, self._y + other, self._z + other)
        raise TypeError

    def __radd__(self, other: "Vector3 | int | float") -> "Vector3":
        return self.__add__(other)

    def __sub__(self, other: "Vector3 | int | float") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(self._x - other.x,
                           self._y - other.y,
                           self._z - other.z)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(self._x - other, self._y - other, self._z - other)
        raise TypeError

    def __rsub__(self, other: "Vector3 | int | float") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(other.x - self._x,
                           other.y - self._y,
                           other.z - self._z)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(other - self._x, other - self._y, other - self._z)
        raise TypeError

    def __mul__(self, other: "Vector3 | int | float") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(self._x * other.x,
                           self._y * other.y,
                           self._z * other.z)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(self._x * other, self._y * other, self._z * other)
        raise TypeError

    def __rmul__(self, other: "Vector3 | int | float") -> "Vector3":
        return self.__mul__(other)

    def normalize(self) -> bool:
        magnitude = self.magnitude
        if not magnitude:
            return False
        self._x /= magnitude
        self._y /= magnitude
        self._z /= magnitude
        return True
