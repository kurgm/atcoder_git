import functools
import time
from typing import Callable, Optional, TypeVar


__all__ = [
    "limit_interval",
    "wait_until",
]


def wait_until(t: float) -> None:
    now = time.time()
    if now < t:
        time.sleep(t - now)


def limit_interval(interval: float):
    next_time: Optional[float] = None
    RT = TypeVar("RT")

    def _limit_interval(func: Callable[..., RT]) -> Callable[..., RT]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal next_time
            if next_time is not None:
                wait_until(next_time)

            result = func(*args, **kwargs)

            next_time = time.time() + interval
            return result
        return wrapper

    return _limit_interval
