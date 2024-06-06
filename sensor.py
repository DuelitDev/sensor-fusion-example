import socket
import struct
import threading


class Sensor:
    ax = property(fget=lambda self: self._ax)
    ay = property(fget=lambda self: self._ay)
    az = property(fget=lambda self: self._az)
    gx = property(fget=lambda self: self._gx)
    gy = property(fget=lambda self: self._gy)
    gz = property(fget=lambda self: self._gz)
    mx = property(fget=lambda self: self._mx)
    my = property(fget=lambda self: self._my)
    mz = property(fget=lambda self: self._mz)
    pressure = property(fget=lambda self: self._pressure)
    temperature = property(fget=lambda self: self._temperature)

    def __init__(self, port: int = 8888):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(("0.0.0.0", port))
        self._ax, self._ay, self._az = 0, 0, 0
        self._gx, self._gy, self._gz = 0, 0, 0
        self._mx, self._my, self._mz = 0, 0, 0
        self._pressure, self._temperature = 0, 23.5
        threading.Thread(target=self._update, daemon=True).start()

    def _update(self):
        while True:
            data, addr = self._sock.recvfrom(13)
            if data[0] == 1:
                self._ax = struct.unpack("<f", data[1:5])[0]
                self._ay = struct.unpack("<f", data[5:9])[0]
                self._az = struct.unpack("<f", data[9:13])[0]
            if data[0] == 4:
                self._gx = struct.unpack("<f", data[1:5])[0]
                self._gy = struct.unpack("<f", data[5:9])[0]
                self._gz = struct.unpack("<f", data[9:13])[0]
            if data[0] == 2:
                self._mx = struct.unpack("<f", data[1:5])[0]
                self._my = struct.unpack("<f", data[5:9])[0]
                self._mz = struct.unpack("<f", data[9:13])[0]
            if data[0] == 6:
                self._pressure = struct.unpack("<f", data[1:5])[0]
