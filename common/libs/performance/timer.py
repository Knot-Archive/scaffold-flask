# file:timer.py
# summary:计时器 用来记录一段逻辑运行需要的时间
import time


class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def countdown(n):
    while n > 0:
        n -= 1


if __name__ == '__main__':
    # Use 1: Explicit start/stop
    t = Timer()
    t.start()
    countdown(1000000)
    t.stop()
    print(t.elapsed)

    # Use 2: As a context manager
    with t:
        countdown(1000000)

    print(t.elapsed)

    with Timer() as t2:
        countdown(1000000)
    print(t2.elapsed)
