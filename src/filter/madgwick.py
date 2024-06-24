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
        if not a.normalize() or not m.normalize():
            return False
        q_dot = .5 * q * Quaternion(0, g.x, g.y, g.z)
        h = q * Quaternion(0, m.x, m.y, m.z) * ~q
        b = math.sqrt(h.x ** 2 + h.y ** 2)
        # Gradient decent algorithm corrective step
        w2, x2, y2, z2 = 2 * q.w, 2 * q.x, 2 * q.y, 2 * q.z
        xq, yq, zq = q.x * q.x, q.y * q.y, q.z * q.z
        hxy, hzx, hzy = h.x * h.y, h.z * h.x, h.z * h.y
        xz_yw, wx_yz, xy_wz, wy_xz = ((q.x * q.z) - (q.w * q.y),
                                      (q.w * q.x) + (q.y * q.z),
                                      (q.x * q.y) - (q.w * q.z),
                                      (q.w * q.y) + (q.x * q.z))
        fb, fh, fm, fa = b * (.5 - yq - zq), hzx * xz_yw, m.x, a.x
        t1, t2, t3 = ((x2 * wx_yz - a.y),
                      h.z * (b * xy_wz + hzx * wx_yz - m.y),
                      b * (b * wy_xz + hzy * (.5 - xq - yq) - m.z))
        f = fb + fh - fm
        t23 = t2 + t3

        s0 = -(y2 * xz_yw - t1 - q.y * f + t23)
        s1 = (z2 * xz_yw + w2 * wx_yz - 4 * q.x *
              (1 - 2 * xq - 2 * yq - a.z) + h.z * q.z * f + t23)
        s2 = -(w2 * xz_yw + z2 * wx_yz - 4 * q.y * (1 - 2 * xq - 2 * yq - a.z) +
               (-2 * b * q.y - h.z * q.w) * f + t23)
        s3 = (x2 * xz_yw + y2 * wx_yz + (-2 * b * q.z + hzx) * f + t23)
        s = Quaternion(s0, s1, s2, s3)
        s.normalize()
        q_dot -= Quaternion(self._beta * s.w, self._beta * s.x,
                            self._beta * s.y, self._beta * s.z)
        q += Quaternion(q_dot.w, q_dot.x, q_dot.y, q_dot.z) * dt
        q.normalize()
        self._quaternion = q
        return True
