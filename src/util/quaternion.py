import math
from src.util.vector import Vector3

__all__ = [
    "Quaternion"
]


class Quaternion:
    @property
    def w(self) -> float:
        return self._w

    @w.setter
    def w(self, value: float):
        self._w = value

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
    def euler_angles(self) -> Vector3:
        w, x, y, z = self._w, self._x, self._y, self._z
        roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
        pitch = math.asin(1 if (i := 2 * (w * y - z * x)) > 1
                          else (-1 if i < -1 else i))
        yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
        return Vector3(roll, pitch, yaw)

    def __init__(self, w: float, x: float, y: float, z: float):
        self._w, self._x, self._y, self._z = w, x, y, z

    def __repr__(self) -> str:
        return f"Quaternion({self._w}, {self._x}, {self._y}, {self._z})"

    def __invert__(self) -> "Quaternion":
        return Quaternion(self._w, -self._x, -self._y, -self._z)

    def __add__(self, other: "Quaternion | int | float") -> "Quaternion":
        if isinstance(other, Quaternion):
            return Quaternion(self._w + other.w,
                              self._x + other.x,
                              self._y + other.y,
                              self._z + other.z)
        elif isinstance(other, int) or isinstance(other, float):
            return Quaternion(self._w + other,
                              self._x + other,
                              self._y + other,
                              self._z + other)
        raise TypeError

    def __radd__(self, other: "Quaternion | int | float") -> "Quaternion":
        return self.__add__(other)

    def __sub__(self, other: "Quaternion | int | float") -> "Quaternion":
        if isinstance(other, Quaternion):
            return Quaternion(self._w - other.w,
                              self._x - other.x,
                              self._y - other.y,
                              self._z - other.z)
        elif isinstance(other, int) or isinstance(other, float):
            return Quaternion(self._w - other,
                              self._x - other,
                              self._y - other,
                              self._z - other)
        raise TypeError

    def __rsub__(self, other: "Quaternion | int | float") -> "Quaternion":
        if isinstance(other, Quaternion):
            return Quaternion(other.w - self._w,
                              other.x - self._x,
                              other.y - self._y,
                              other.z + self._z)
        elif isinstance(other, int) or isinstance(other, float):
            return Quaternion(other - self._w,
                              other - self._x,
                              other - self._y,
                              other + self._z)
        raise TypeError

    def __mul__(self, other: "Quaternion | int | float") -> "Quaternion":
        if isinstance(other, Quaternion):
            w1, x1, y1, z1 = self._w, self._x, self._y, self._z
            w2, x2, y2, z2 = other.w, other.x, other.y, other.z
            return Quaternion(w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                              w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                              w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                              w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2)
        elif isinstance(other, int) or isinstance(other, float):
            return Quaternion(self._w * other,
                              self._x * other,
                              self._y * other,
                              self._z * other)
        else:
            raise ValueError

    def __rmul__(self, other: "Quaternion | int | float") -> "Quaternion":
        return self.__mul__(other)

    def normalize(self) -> bool:
        magnitude = math.sqrt(self._w ** 2 +
                              self._x ** 2 +
                              self._y ** 2 +
                              self._z ** 2)
        if not magnitude:
            return False
        self._w /= magnitude
        self._x /= magnitude
        self._y /= magnitude
        self._z /= magnitude
        return True
