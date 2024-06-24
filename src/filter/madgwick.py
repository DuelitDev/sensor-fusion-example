import math
from src.filter.core import Filter
from src.util import Quaternion, Vector3

__all__ = [
    "MadgwickFilter"
]


class MadgwickFilter(Filter):
    # from hideakitai/MPU9250
    def __init__(self, beta: float = 1, zeta: float = 0):
        super().__init__()
        self._beta = beta
        self._zeta = zeta

    def update(self, a: Vector3, g: Vector3, m: Vector3):
        q = self._quaternion
        dt = self._delta()
        a.normalize()
        m.normalize()
        q_dot = .5 * q * Quaternion(0, g.x, g.y, g.z)
        h = q * Quaternion(0, m.x, m.y, m.z) * ~q
        b = math.sqrt(h.x ** 2 + h.y ** 2)
        s0 = (-(2 * q.y) * (2 * (q.x * q.z) - (2 * q.w * q.y) - a.x) + (2 * q.x) * (2 * (q.w * q.x) + (2 * q.y * q.z) - a.y) - h.z * q.y * (b * (.5 - (q.y * q.y) - (q.z * q.z)) + h.z * ((q.x * q.z) - (q.w * q.y)) - m.x) + (-b * q.z + h.z * q.x) * (b * ((q.x * q.y) - (q.w * q.z)) + h.z * ((q.w * q.x) + (q.y * q.z)) - m.y) + b * q.y * (b * ((q.w * q.y) + (q.x * q.z)) + h.z * (.5 - (q.x * q.x) - (q.y * q.y)) - m.z))
        s1 = ((2 * q.z) * (2 * (q.x * q.z) - (2 * q.w * q.y) - a.x) + (2 * q.w) * (2 * (q.w * q.x) + (2 * q.y * q.z) - a.y) - 4 * q.x * (1 - 2 * (q.x * q.x) - 2 * (q.y * q.y) - a.z) + h.z * q.z * (b * (.5 - (q.y * q.y) - (q.z * q.z)) + h.z * ((q.x * q.z) - (q.w * q.y)) - m.x) + (b * q.y + h.z * q.w) * (b * ((q.x * q.y) - (q.w * q.z)) + h.z * ((q.w * q.x) + (q.y * q.z)) - m.y) + (b * q.z - (2 * h.z) * q.x) * (b * ((q.w * q.y) + (q.x * q.z)) + h.z * (.5 - (q.x * q.x) - (q.y * q.y)) - m.z))
        s2 = (-(2 * q.w) * (2 * (q.x * q.z) - (2 * q.w * q.y) - a.x) + (2 * q.z) * (2 * (q.w * q.x) + (2 * q.y * q.z) - a.y) - 4 * q.y * (1 - 2 * (q.x * q.x) - 2 * (q.y * q.y) - a.z) + (-(2 * b) * q.y - h.z * q.w) * (b * (.5 - (q.y * q.y) - (q.z * q.z)) + h.z * ((q.x * q.z) - (q.w * q.y)) - m.x) + (b * q.x + h.z * q.z) * (b * ((q.x * q.y) - (q.w * q.z)) + h.z * ((q.w * q.x) + (q.y * q.z)) - m.y) + (b * q.w - (2 * h.z) * q.y) * (b * ((q.w * q.y) + (q.x * q.z)) + h.z * (.5 - (q.x * q.x) - (q.y * q.y)) - m.z))
        s3 = ((2 * q.x) * (2 * (q.x * q.z) - (2 * q.w * q.y) - a.x) + (2 * q.y) * (2 * (q.w * q.x) + (2 * q.y * q.z) - a.y) + (-(2 * b) * q.z + h.z * q.x) * (b * (.5 - (q.y * q.y) - (q.z * q.z)) + h.z * ((q.x * q.z) - (q.w * q.y)) - m.x) + (-b * q.w + h.z * q.y) * (b * ((q.x * q.y) - (q.w * q.z)) + h.z * ((q.w * q.x) + (q.y * q.z)) - m.y) + b * q.x * (b * ((q.w * q.y) + (q.x * q.z)) + h.z * (.5 - (q.x * q.x) - (q.y * q.y)) - m.z))
        s = Quaternion(s0, s1, s2, s3)
        s.normalize()
        q_dot -= Quaternion(self._beta * s.w, self._beta * s.x,
                            self._beta * s.y, self._beta * s.z)
        q += Quaternion(q_dot.w * dt, q_dot.x * dt, q_dot.y * dt, q_dot.z * dt)
        q.normalize()
        self._quaternion = q
        return True
