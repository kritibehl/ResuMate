import time
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class TimerResult:
    started_at: float
    ended_at: float | None = None

    @property
    def elapsed_ms(self) -> int:
        end = self.ended_at if self.ended_at is not None else time.perf_counter()
        return int((end - self.started_at) * 1000)


@contextmanager
def timed():
    result = TimerResult(started_at=time.perf_counter())
    try:
        yield result
    finally:
        result.ended_at = time.perf_counter()
