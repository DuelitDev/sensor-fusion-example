from abc import ABCMeta, abstractmethod
from ins.util import Quaternion, Vector3
from time import time

__all__ = [
    "Filter"
]


class Filter(metaclass=ABCMeta):
    @property
    def quaternion(self) -> Quaternion:
        return self._quaternion

    def __init__(self):
        self._last = time()
        self._quaternion = Quaternion(1, 0, 0, 0)

    def _delta(self) -> float:
        now = time()
        dt = now - self._last
        self._last = now
        return dt

    @abstractmethod
    def update(self, a: Vector3, g: Vector3, m: Vector3) -> bool:
        pass
