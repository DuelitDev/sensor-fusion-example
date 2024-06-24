from src.filter.core import Filter
from src.util import Quaternion, Vector3

__all__ = [
    "Madgwick2Filter"
]


class Madgwick2Filter(Filter):
    # from morgil/madgwick_py
    def __init__(self, beta: float = 1, zeta: float = 0):
        super().__init__()
        self._beta = beta
        self._zeta = zeta

    def update(self, a: Vector3, g: Vector3, m: Vector3) -> bool:
        q = self._quaternion
        dt = self._delta()
        if not a.normalize() or not m.normalize():
            return False
        h = q * (Quaternion(0, m.x, m.y, m.z) * ~q)
        b1 = Vector3(h.x, h.y, h.z).magnitude
        b3 = h.z
        f0 = 2 * (q.x * q.z - q.w * q.y) - a.x
        f1 = 2 * (q.w * q.x + q.y * q.z) - a.y
        f2 = 2 * (.5 - q.x ** 2 - q.y ** 2) - a.z
        f3 = (2 * b1 * (.5 - q.y ** 2 - q.z ** 2) +
              2 * b3 * (q.x * q.z - q.w * q.y) - m.x)
        f4 = (2 * b1 * (q.x * q.y - q.w * q.z) +
              2 * b3 * (q.w * q.x + q.y * q.z) - m.y)
        f5 = (2 * b1 * (q.w * q.y + q.x * q.z) +
              2 * b3 * (.5 - q.x ** 2 - q.y ** 2) - m.z)
        j00, j01, j02, j03 = -2 * q.y, 2 * q.z, -2 * q.w, 2 * q.x
        j10, j11, j12, j13 = 2 * q.x, 2 * q.w, 2 * q.z, 2 * q.y
        j20, j21, j22, j23 = 0, -4 * q.x, -4 * q.y, 0
        j30, j31, j32, j33 = (-2 * b3 * q.y, 2 * b3 * q.z,
                              -4 * b1 * q.y - 2 * b3 * q.w,
                              -4 * b1 * q.z + 2 * b3 * q.x)
        j40, j41, j42, j43 = (-2 * b1 * q.z + 2 * b3 * q.x,
                              2 * b1 * q.y + 2 * b3 * q.w,
                              2 * b1 * q.x + 2 * b3 * q.z,
                              -2 * b1 * q.w + 2 * b3 * q.y)
        j50, j51, j52, j53 = (2 * b1 * q.y, 2 * b1 * q.z - 4 * b3 * q.x,
                              2 * b1 * q.w - 4 * b3 * q.y, 2 * b1 * q.x)
        step = Quaternion(
            j00 * f0 + j10 * f1 + j20 * f2 + j30 * f3 + j40 * f4 + j50 * f5,
            j01 * f0 + j11 * f1 + j21 * f2 + j31 * f3 + j41 * f4 + j51 * f5,
            j02 * f0 + j12 * f1 + j22 * f2 + j32 * f3 + j42 * f4 + j52 * f5,
            j03 * f0 + j13 * f1 + j23 * f2 + j33 * f3 + j43 * f4 + j53 * f5)
        step.normalize()
        gq = Quaternion(0, g.x, g.y, g.z)
        gq = gq + (~q * step) * 2 * dt * self._zeta * -1
        q_dot = (q * gq) * .5 - self._beta * step
        q += q_dot * dt
        q.normalize()
        self._quaternion = q
        return True
