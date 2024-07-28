from math import sin, radians as rad
from src.filter.core import Filter
from src.util import Quaternion, Vector3

__all__ = [
    "FusionFilterOptions",
    "FusionFilter"
]


class FusionFilterOptions:
    def __init__(self, *,
                 gain:            float = 0.5,
                 initial_gain:    float = 10.0,
                 initial_period:  float = 3.0,
                 acc_rejection:   float = 10.0,
                 gyr_range:       float = 0.0,
                 mag_rejection:   float = 10.0,
                 recovery_period: int   = 600):
        def rejection(v: float) -> float:
            return float("inf") if v == 0 else 0.5 * sin(rad(v)) ** 2.0

        self._gain:            float = gain
        self._initial_gain:    float = initial_gain
        self._initial_period:  float = initial_period
        self._acc_rejection:   float = rejection(acc_rejection)
        self._gyr_range:       float = gyr_range
        self._mag_rejection:   float = rejection(mag_rejection)
        self._recovery_period: int   = 0 if gain == 0.0 else recovery_period

    @property
    def gain(self) -> float:
        return self._gain

    @gain.setter
    def gain(self, value: float):
        self._gain = value

    @property
    def initial_gain(self) -> float:
        return self._initial_gain

    @initial_gain.setter
    def initial_gain(self, value: float):
        self._initial_gain = value

    @property
    def initial_period(self) -> float:
        return self._initial_period

    @initial_period.setter
    def initial_period(self, value: float):
        self._initial_period = value

    @property
    def gyr_range(self) -> float:
        return self._gyr_range

    @gyr_range.setter
    def gyr_range(self, value: float):
        self._gyr_range = value

    @property
    def acc_rejection(self) -> float:
        return self._acc_rejection

    @acc_rejection.setter
    def acc_rejection(self, value: float):
        self._acc_rejection = value

    @property
    def mag_rejection(self) -> float:
        return self._mag_rejection

    @mag_rejection.setter
    def mag_rejection(self, value: float):
        self._mag_rejection = value

    @property
    def recovery_period(self) -> int:
        return self._recovery_period

    @recovery_period.setter
    def recovery_period(self, value: int):
        self._recovery_period = value


class FusionFilter(Filter):
    # from xioTechnologies/Fusion
    def __init__(self, configure: FusionFilterOptions = FusionFilterOptions()):
        super().__init__()
        self._initializing:         bool    = False
        self._gain:                 float   = 0.0
        self._initial_gain:         float   = 0.0
        self._ramped_gain:          float   = 0.0
        self._ramped_gain_step:     float   = 0.0
        self._recovery_period:      int     = 0
        self._acc_rejection:        float   = 0.0
        self._acc_half_feedback:    Vector3 = Vector3.zero
        self._acc_recovery_trigger: int     = 0
        self._acc_recovery_timeout: int     = 0
        self._gyr_range:            float   = 0.0
        self._gyr_recovery:         bool    = False
        self._mag_rejection:        float   = 0.0
        self._mag_half_feedback:    Vector3 = Vector3.zero
        self._mag_recovery_trigger: int     = 0
        self._mag_recovery_timeout: int     = 0
        self.configure(configure)
        self.reset()

    def configure(self, opt: FusionFilterOptions):
        self._gain = opt.gain
        self._initial_gain = opt.initial_gain
        self._gyr_range = (float("inf") if opt.gyr_range == 0.0
                           else 0.98 * opt.gyr_range)
        self._acc_rejection = opt.acc_rejection
        self._mag_rejection = opt.mag_rejection
        self._recovery_period = opt.recovery_period
        self._acc_recovery_timeout = self._recovery_period
        self._mag_recovery_timeout = self._recovery_period
        if not self._initializing:
            self._ramped_gain = self._gain
        self._ramped_gain_step = (
                (self._initial_gain - self._gain) / opt.initial_period)

    def reset(self):
        self._quaternion = Quaternion.identity
        self._initializing = True
        self._ramped_gain = self._initial_gain
        self._acc_half_feedback = Vector3.zero
        self._acc_recovery_trigger = 0
        self._gyr_recovery = False
        self._mag_half_feedback = Vector3.zero
        self._mag_recovery_trigger = 0

    def update(self, a: Vector3, g: Vector3, m: Vector3) -> bool:
        dt = self._delta()
        if abs(g.x) <= self._gyr_range:
            pass
        elif abs(g.y) <= self._gyr_range:
            pass
        elif abs(g.z) <= self._gyr_range:
            pass
        else:
            temp = self._quaternion
            self.reset()
            self._quaternion = temp
            self._gyr_recovery = True

        if self._initializing:
            self._ramped_gain -= self._ramped_gain_step * dt
            if self._ramped_gain < self._gain or self._gain == 0.0:
                self._ramped_gain = self._gain
                self._initializing = False
                self._gyr_recovery = False

        hg = self._half_gravity()
        ahf = Vector3.zero
        acc_ignored = True
        if a.normalized():
            ahf = self._feedback(a, hg)
            if self._initializing or ahf.magnitude ** 2 <= self._acc_rejection:
                self._acc_recovery_trigger -= 9
                acc_ignored = False
            else:
                self._acc_recovery_trigger += 1
            if self._acc_recovery_trigger > self._acc_recovery_timeout:
                self._acc_recovery_timeout = 0
                acc_ignored = False
            else:
                self._acc_recovery_timeout = self._recovery_period
            self._acc_recovery_trigger = self._clamp(
                self._acc_recovery_trigger,
                0, self._recovery_period)
            if acc_ignored:
                ahf = Vector3.zero

        hm = self._half_magnetic()
        mhf = Vector3.zero
        mag_ignored = True
        if m.magnitude != 0:
            mhf = self._feedback(hg.cross(m).normalize(), hm)
            if self._initializing or mhf.magnitude ** 2 <= self._mag_rejection:
                self._mag_recovery_trigger -= 9
                mag_ignored = False
            else:
                self._mag_recovery_trigger += 1
            if self._mag_recovery_trigger > self._mag_recovery_timeout:
                self._mag_recovery_timeout = 0
                mag_ignored = False
            else:
                self._mag_recovery_timeout = self._recovery_period
            self._mag_recovery_trigger = self._clamp(
                self._mag_recovery_trigger,
                0, self._recovery_period)
            if mag_ignored:
                hmf = Vector3.zero
        ahg = g * rad(0.5) + (ahf + mhf) * self._ramped_gain
        self._quaternion += self._quaternion * (ahg * dt)
        self._quaternion.normalized()
        return True

    def _half_gravity(self) -> Vector3:
        q = self._quaternion
        return Vector3(q.w * q.y - q.x * q.z,
                       -1.0 * (q.y * q.z + q.w * q.x),
                       0.5 - q.w * q.w - q.z * q.z)

    def _half_magnetic(self) -> Vector3:
        q = self._quaternion
        return Vector3(-1.0 * (q.x * q.y + q.w * q.z),
                       0.5 - q.w * q.w - q.y * q.y,
                       q.w * q.x - q.y * q.z)

    @staticmethod
    def _feedback(sensor: Vector3, ref: Vector3) -> Vector3:
        if sensor @ ref < 0:
            return sensor.cross(ref).normalize()
        return sensor.cross(ref)

    @staticmethod
    def _clamp(value: int, min_: int, max_: int) -> int:
        return min_ if value < min_ else max_ if value > max_ else value
