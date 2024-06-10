import math
import time
from util import *


class MahonyFilter:
    @property
    def quaternion(self) -> Quaternion:
        return self._quaternion

    def __init__(self, beta: float = 4.0, zeta: float = 1.0):
        self._kp = 40
        self._ki = 0
        self._last = time.time()
        self._integral = Vector3(0, 0, 0)
        self._quaternion = Quaternion(1, 0, 0, 0)

    def update(self, a: Vector3, g: Vector3, m: Vector3):
        delta = time.time() - self._last
        q = self._quaternion
        kp, ki = self._kp, self._ki
        i = self._integral

        # Compute feedback only if accelerometer measurement valid
        if a.magnitude > 0.0:
            a.normalize()

            # Estimated direction of gravity in the body frame
            vx = q.x * q.z - q.w * q.y
            vy = q.w * q.x + q.y * q.z
            vz = q.w * q.w - 0.5 + q.z * q.z

            # Error is cross product between estimated and measured direction of gravity in body frame
            ex = a.y * vz - a.z * vy
            ey = a.z * vx - a.x * vz
            ez = a.x * vy - a.y * vx

            # Compute and apply to gyro term the integral feedback, if enabled
            if ki > 0.0:
                i.x += ki * ex * delta
                i.y += ki * ey * delta
                i.z += ki * ez * delta
                g.x += i.x
                g.y += i.y
                g.z += i.z

            # Apply proportional feedback to gyro term
            g.x += kp * ex
            g.y += kp * ey
            g.z += kp * ez

        # Integrate rate of change of quaternion, q cross gyro term
        delta_half = 0.5 * delta
        g.x *= delta_half
        g.y *= delta_half
        g.z *= delta_half

        q_dot = Quaternion(0, g.x, g.y, g.z) * q
        self._quaternion = q + q_dot

        # Renormalize quaternion
        self._quaternion.normalize()



sensor = Sensor()
mahony = MahonyFilter()


while True:
    time.sleep(0.001)
    mahony.update(Vector3(-sensor.ay, -sensor.ax, sensor.az),
                  Vector3(-sensor.gy, -sensor.gx, sensor.gz),
                  Vector3(-sensor.my, -sensor.mx, sensor.mz))
    v = mahony.quaternion.euler_angles
    roll = v.x * (180 / math.pi)
    pitch = v.y * (180 / math.pi)
    yaw = v.z * (180 / math.pi) + 180
    print(f"{roll: 6.2f}, {pitch: 6.2f}, {yaw: 6.2f}")


