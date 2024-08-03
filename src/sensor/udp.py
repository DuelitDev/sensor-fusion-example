from math import degrees as deg
from struct import unpack
from socket import AF_INET, SOCK_DGRAM, socket
from src.filter.core import Filter
from src.sensor.core import Sensor

__all__ = [
    "UDPSensor"
]


# Arduino Serial Sensor app
class UDPSensor(Sensor):
    def __init__(self, filter_: Filter, address: str, port: int):
        super().__init__(filter_)
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.bind((address, port))

    def _update(self):
        while True:
            data, addr = self._sock.recvfrom(13)
            if data[0] == 1:
                self._set_acc_from_opt(
                    unpack("<f", data[1:5])[0] / 9.81,
                    unpack("<f", data[5:9])[0] / 9.81,
                    unpack("<f", data[9:])[0]  / 9.81)
            if data[0] == 4:
                self._set_gyr_from_opt(
                    deg(unpack("<f", data[1:5])[0]),
                    deg(unpack("<f", data[5:9])[0]),
                    deg(unpack("<f", data[9:])[0]))
            if data[0] == 2:
                self._set_mag_from_opt(
                    unpack("<f", data[1:5])[0],
                    unpack("<f", data[5:9])[0],
                    unpack("<f", data[9:])[0])
            self._filter.update(self.av, self.gv, self.mv)

