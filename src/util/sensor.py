import enum
import socket
import struct
import threading
from src.util.vector import Vector3

__all__ = [
    "Order",
    "Sensor"
]


class Order(enum.Enum):
    XYZ = (0, 1, 2)
    XZY = (0, 2, 1)
    YXZ = (1, 0, 2)
    YZX = (1, 2, 0)
    ZXY = (2, 0, 1)
    ZYX = (2, 1, 0)


# Arduino Serial Sensor app
class Sensor:
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
    def ax(self) -> float:
        return self._ax * (1 - self._invert[0][0] * 2)

    @property
    def ay(self) -> float:
        return self._ay * (1 - self._invert[0][1] * 2)

    @property
    def az(self) -> float:
        return self._az * (1 - self._invert[0][2] * 2)

    @property
    def gx(self) -> float:
        return self._gx * (1 - self._invert[1][0] * 2)

    @property
    def gy(self) -> float:
        return self._gy * (1 - self._invert[1][1] * 2)

    @property
    def gz(self) -> float:
        return self._gz * (1 - self._invert[1][2] * 2)

    @property
    def mx(self) -> float:
        return self._mx * (1 - self._invert[2][0] * 2)

    @property
    def my(self) -> float:
        return self._my * (1 - self._invert[2][1] * 2)

    @property
    def mz(self) -> float:
        return self._mz * (1 - self._invert[2][2] * 2)

    @property
    def av(self) -> Vector3:
        return Vector3(self.ax, self.ay, self.az)

    @property
    def gv(self) -> Vector3:
        return Vector3(self.gx, self.gy, self.gz)

    @property
    def mv(self) -> Vector3:
        return Vector3(self.mx, self.my, self.mz)

    @property
    def pressure(self) -> float:
        return self._pressure

    @property
    def temperature(self) -> float:
        return self._temperature

    def __init__(self, port: int = 8888):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(("0.0.0.0", port))
        self._order = (Order.XYZ, Order.XYZ, Order.XYZ)
        self._invert = ((False, False, False),
                        (False, False, False),
                        (False, False, False))
        self._ax, self._ay, self._az = 0, 0, 0
        self._gx, self._gy, self._gz = 0, 0, 0
        self._mx, self._my, self._mz = 0, 0, 0
        self._pressure, self._temperature = 0, 23.5
        threading.Thread(target=self._update, daemon=True).start()

    def _update(self):
        while True:
            data, addr = self._sock.recvfrom(13)
            if data[0] == 1:
                temp = (struct.unpack("<f", data[1:5])[0],
                        struct.unpack("<f", data[5:9])[0],
                        struct.unpack("<f", data[9:13])[0])
                self._ax, self._ay, self._az = (
                    temp[self._order[0].value[0]],
                    temp[self._order[0].value[1]],
                    temp[self._order[0].value[2]])
            if data[0] == 4:
                temp = (struct.unpack("<f", data[1:5])[0],
                        struct.unpack("<f", data[5:9])[0],
                        struct.unpack("<f", data[9:13])[0])
                self._gx, self._gy, self._gz = (
                    temp[self._order[1].value[0]],
                    temp[self._order[1].value[1]],
                    temp[self._order[1].value[2]])
            if data[0] == 2:
                temp = (struct.unpack("<f", data[1:5])[0],
                        struct.unpack("<f", data[5:9])[0],
                        struct.unpack("<f", data[9:13])[0])
                self._mx, self._my, self._mz = (
                    temp[self._order[2].value[0]],
                    temp[self._order[2].value[1]],
                    temp[self._order[2].value[2]])
            if data[0] == 6:
                self._pressure = struct.unpack("<f", data[1:5])[0]
