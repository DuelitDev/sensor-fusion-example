import abc
import time
from src.util import *

__all__ = [
    "Filter"
]


class Filter(metaclass=abc.ABCMeta):
    @property
    def quaternion(self) -> Quaternion:
        return self._quaternion

    def __init__(self):
        self._last = time.time()
        self._quaternion = Quaternion(1, 0, 0, 0)

    def _delta(self) -> float:
        now = time.time()
        dt = now - self._last
        self._last = now
        return dt

    @abc.abstractmethod
    def update(self, a: Vector3, g: Vector3, m: Vector3) -> bool:
        pass
