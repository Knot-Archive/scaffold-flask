# file:timeblock.py
# summary:测量块代码时间
import time
from contextlib import contextmanager


@contextmanager
def timeblock(label):
    "要测试某个代码块运行时间，你可以定义一个上下文管理器"
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('{} : {}'.format(label, end - start))


"""
>>> with timeblock('counting'):
...     n = 10000000
...     while n > 0:
...             n -= 1
...
counting : 1.5551159381866455
>>>
"""
