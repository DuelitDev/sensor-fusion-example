import math

__all__ = [
    "Vector3"
]


class Vector3:
    zero: "Vector3"

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
    def magnitude(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

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

    def __neg__(self) -> "Vector3":
        return Vector3(-self._x, -self._y, -self._z)

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

    def __truediv__(self, other: "Vector3 | int | float") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(self._x / other.x,
                           self._y / other.y,
                           self._z / other.z)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(self._x / other, self._y / other, self._z / other)
        raise TypeError

    def __rtruediv__(self, other: "Vector3 | int | float") -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(other.x / self._x,
                           other.y / self._y,
                           other.z / self._z)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(other / self._x, other / self._y, other / self._z)
        raise TypeError

    def __matmul__(self, other: "Vector3") -> float:
        return self.dot(other)

    def __rmatmul__(self, other: "Vector3") -> float:
        return other.dot(self)

    def dot(self, other: "Vector3") -> float:
        return self._x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3") -> "Vector3":
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def normalized(self) -> bool:
        magnitude = self.magnitude
        if not magnitude:
            return False
        self._x /= magnitude
        self._y /= magnitude
        self._z /= magnitude
        return True

    def normalize(self) -> "Vector3":
        magnitude = self.magnitude
        if not magnitude:
            return Vector3.zero
        return Vector3(self._x / magnitude,
                       self._y / magnitude,
                       self._z / magnitude)


Vector3.zero = Vector3(0.0, 0.0, 0.0)
