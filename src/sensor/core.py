from abc import ABCMeta, abstractmethod
from enum import Enum
from threading import Thread
from src.filter.core import Filter
from src.util import Quaternion, Vector3

__all__ = [
    "Order",
    "Sensor"
]


class Order(Enum):
    XYZ = (0, 1, 2)
    XZY = (0, 2, 1)
    YXZ = (1, 0, 2)
    YZX = (1, 2, 0)
    ZXY = (2, 0, 1)
    ZYX = (2, 1, 0)


# Arduino Serial Sensor app
class Sensor(metaclass=ABCMeta):
    @property
    def order(self) -> tuple[Order, Order, Order]:
        return self._order

    def set_order(self, *,
                  a: Order = Order.XYZ,
                  g: Order = Order.XYZ,
                  m: Order = Order.XYZ):
        self._order = a, g, m

    @property
    def invert(self) -> tuple[tuple[bool, bool, bool],
                              tuple[bool, bool, bool],
                              tuple[bool, bool, bool]]:
        return self._invert

    def set_invert(self, *,
                   ax: bool = False, ay: bool = False, az: bool = False,
                   gx: bool = False, gy: bool = False, gz: bool = False,
                   mx: bool = False, my: bool = False, mz: bool = False):
        self._invert = ((ax, ay, az), (gx, gy, gz), (mx, my, mz))

    @property
    def calibrate(self) -> tuple[tuple[float, float, float],
                                 tuple[float, float, float],
                                 tuple[float, float, float]]:
        return self._calibrate

    def set_calibrate(self, *,
                      ax: float = 0.0, ay: float = 0.0, az: float = 0.0,
                      gx: float = 0.0, gy: float = 0.0, gz: float = 0.0,
                      mx: float = 0.0, my: float = 0.0, mz: float = 0.0):
        self._calibrate = ((ax, ay, az), (gx, gy, gz), (mx, my, mz))

    @property
    def ax(self) -> float:
        return self._ax

    @property
    def ay(self) -> float:
        return self._ay

    @property
    def az(self) -> float:
        return self._az

    @property
    def gx(self) -> float:
        return self._gx

    @property
    def gy(self) -> float:
        return self._gy

    @property
    def gz(self) -> float:
        return self._gz

    @property
    def mx(self) -> float:
        return self._mx

    @property
    def my(self) -> float:
        return self._my

    @property
    def mz(self) -> float:
        return self._mz

    @property
    def av(self) -> Vector3:
        return Vector3(self._ax, self._ay, self._az)

    @property
    def gv(self) -> Vector3:
        return Vector3(self._gx, self._gy, self._gz)

    @property
    def mv(self) -> Vector3:
        return Vector3(self._mx, self._my, self._mz)

    @property
    def quaternion(self) -> Quaternion:
        return self._filter.quaternion

    @property
    def euler_angles(self) -> Vector3:
        return self._filter.quaternion.euler_angles

    def _set_acc_from_opt(self, x, y, z):
        temp = (x, y, z)
        self._ax, self._ay, self._az = (
            temp[self._order[0].value[0]],
            temp[self._order[0].value[1]],
            temp[self._order[0].value[2]])
        self._ax *= (1 - self._invert[0][0] * 2)
        self._ay *= (1 - self._invert[0][1] * 2)
        self._az *= (1 - self._invert[0][2] * 2)
        self._ax += self._calibrate[0][0]
        self._ay += self._calibrate[0][1]
        self._az += self._calibrate[0][2]
        self._ax = round(self._ax, 6)
        self._ay = round(self._ay, 6)
        self._az = round(self._az, 6)

    def _set_gyr_from_opt(self, x, y, z):
        temp = (x, y, z)
        self._gx, self._gy, self._gz = (
            temp[self._order[1].value[0]],
            temp[self._order[1].value[1]],
            temp[self._order[1].value[2]])
        self._gx *= (1 - self._invert[1][0] * 2)
        self._gy *= (1 - self._invert[1][1] * 2)
        self._gz *= (1 - self._invert[1][2] * 2)
        self._gx += self._calibrate[1][0]
        self._gy += self._calibrate[1][1]
        self._gz += self._calibrate[1][2]
        self._gx = round(self._gx, 6)
        self._gy = round(self._gy, 6)
        self._gz = round(self._gz, 6)

    def _set_mag_from_opt(self, x, y, z):
        temp = (x, y, z)
        self._mx, self._my, self._mz = (
            temp[self._order[2].value[0]],
            temp[self._order[2].value[1]],
            temp[self._order[2].value[2]])
        self._mx *= (1 - self._invert[2][0] * 2)
        self._my *= (1 - self._invert[2][1] * 2)
        self._mz *= (1 - self._invert[2][2] * 2)
        self._mx += self._calibrate[2][0]
        self._my += self._calibrate[2][1]
        self._mz += self._calibrate[2][2]
        self._mx = round(self._mx, 6)
        self._my = round(self._my, 6)
        self._mz = round(self._mz, 6)

    def __init__(self, filter_: Filter):
        self._order = (Order.XYZ, Order.XYZ, Order.XYZ)
        self._invert = ((False, False, False),
                        (False, False, False),
                        (False, False, False))
        self._calibrate = ((0.0, 0.0, 0.0),
                           (0.0, 0.0, 0.0),
                           (0.0, 0.0, 0.0))
        self._ax, self._ay, self._az = 0, 0, 0
        self._gx, self._gy, self._gz = 0, 0, 0
        self._mx, self._my, self._mz = 0, 0, 0
        self._filter: Filter = filter_
        Thread(target=self._update, daemon=True).start()

    @abstractmethod
    def _update(self):
        pass
