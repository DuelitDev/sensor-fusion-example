from serial import Serial
from ins.filter.core import Filter
from ins.sensor.core import Sensor

__all__ = [
    "SerialSensor"
]


# Serial, MPU9250
class SerialSensor(Sensor):
    @property
    def acc_fs_sel(self) -> int:
        return self._acc_fs_sel

    @acc_fs_sel.setter
    def acc_fs_sel(self, value: int):
        self._acc_fs_sel = value

    @property
    def gyr_fs_sel(self) -> int:
        return self._gyr_fs_sel

    @gyr_fs_sel.setter
    def gyr_fs_sel(self, value: int):
        self._gyr_fs_sel = value

    def __init__(self, filter_: Filter, port: str, baud: int = 115200):
        self._acc_fs_sel: int = 4
        self._gyr_fs_sel: int = 500
        self._serial = Serial(port=port, baudrate=baud)
        super().__init__(filter_)

    def _update(self):
        while True:
            if self._serial.readable():
                try:
                    v = self._serial.readline()[:-1].decode("utf-8")
                    ax, ay, az, gx, gy, gz, mx, my, mz = map(int, v.split(","))
                    ax /= 32768 / self._acc_fs_sel
                    ay /= 32768 / self._acc_fs_sel
                    az /= 32768 / self._acc_fs_sel
                    gx /= 32768 / self._gyr_fs_sel
                    gy /= 32768 / self._gyr_fs_sel
                    gz /= 32768 / self._gyr_fs_sel
                    mx /= 32760 / 4912
                    my /= 32760 / 4912
                    mz /= 32760 / 4912
                    self._set_acc_from_opt(ax, ay, az)
                    self._set_gyr_from_opt(gx, gy, gz)
                    self._set_mag_from_opt(mx, my, mz)
                    self._filter.update(self.av, self.gv, self.mv)
                except UnicodeDecodeError:
                    pass
                except ValueError:
                    pass
