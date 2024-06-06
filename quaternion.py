import math
from vector import Vector3


class Quaternion:
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
    def w(self) -> float:
        return self._w

    @property
    def euler_angles(self) -> Vector3:
        w, x, y, z = self._w, self._x, self._y, self._z
        roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
        pitch = math.asin(1 if (i := 2 * (w * y - z * x)) > 1
                          else (-1 if i < -1 else i))
        yaw = math.atan2(2.0 * (w * z + x * y), 1 - 2 * (y * y + z * z))
        return Vector3(roll, pitch, yaw)

    def __init__(self, w: float, x: float, y: float, z: float):
        self._w, self._x, self._y, self._z = w, x, y, z

    def __invert__(self) -> "Quaternion":
        return Quaternion(self._w, -self._x, -self._y, -self._z)

    def __add__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(self._w + other.w,
                          self._x + other.x,
                          self._y + other.y,
                          self._z + other.z)

    def __sub__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(self._w - other.w,
                          self._x - other.x,
                          self._y - other.y,
                          self._z - other.z)

    def __mul__(self, other: "Quaternion | float") -> "Quaternion":
        if isinstance(other, Quaternion):
            w1, x1, y1, z1 = self._w, self._x, self._y, self._z
            w2, x2, y2, z2 = other.w, other.x, other.y, other.z
            return Quaternion(w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                              w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                              w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                              w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2)
        elif isinstance(other, float):
            return Quaternion(self._w * other,
                              self._x * other,
                              self._y * other,
                              self._z * other)
        else:
            raise ValueError

    def __rmul__(self, other: "Quaternion | float") -> "Quaternion":
        return self.__mul__(other)

    def set(self, w: float, x: float, y: float, z: float):
        self._w, self._x, self._y, self._z = w, x, y, z

    def normalize(self):
        magnitude = math.sqrt(self._w ** 2 +
                              self._x ** 2 +
                              self._y ** 2 +
                              self._z ** 2)
        if not magnitude:
            return
        self._w /= magnitude
        self._x /= magnitude
        self._y /= magnitude
        self._z /= magnitude
