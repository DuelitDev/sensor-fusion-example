import struct
import socket
from src.filter.core import Filter
from src.sensor.core import Sensor

__all__ = [
    "UDPSensor"
]


# Arduino Serial Sensor app
class UDPSensor(Sensor):
    def __init__(self, filter_: Filter, port: int = 8888):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(("0.0.0.0", port))
        super().__init__(filter_)

    def _update(self):
        while True:
            data, addr = self._sock.recvfrom(13)
            if data[0] == 1:
                self._set_acc_from_opt(
                    struct.unpack("<f", data[1:5])[0],
                    struct.unpack("<f", data[5:9])[0],
                    struct.unpack("<f", data[9:13])[0])
            if data[0] == 4:
                self._set_gyr_from_opt(
                    struct.unpack("<f", data[1:5])[0],
                    struct.unpack("<f", data[5:9])[0],
                    struct.unpack("<f", data[9:13])[0])
            if data[0] == 2:
                self._set_mag_from_opt(
                    struct.unpack("<f", data[1:5])[0],
                    struct.unpack("<f", data[5:9])[0],
                    struct.unpack("<f", data[9:13])[0])
            self._filter.update(self.av, self.gv, self.mv)

