# file:timethis.py
# summary: 测量函数时间
import logging
import time
from functools import wraps


def timethis_perf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        logging.info('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r

    return wrapper


def timethis_process(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.process_time()
        r = func(*args, **kwargs)
        end = time.process_time()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r

    return wrapper


"""
>>> @timethis_
... def countdown(n):
...     while n > 0:
...             n -= 1
...
>>> countdown(10000000)
__main__.countdown : 0.803001880645752
>>>
"""

"""
当执行性能测试的时候，需要注意的是你获取的结果都是近似值。 
time.perf_counter() 函数会在给定平台上获取最高精度的计时值。 
不过，它仍然还是基于时钟时间，很多因素会影响到它的精确度，比如机器负载。 
如果你对于执行时间更感兴趣，使用 time.process_time() 来代替它。
"""

"""
最后我引用John Ousterhout说过的话作为结尾：“最好的性能优化是从不工作到工作状态的迁移”。 
直到你真的需要优化的时候再去考虑它。
确保你程序正确的运行通常比让它运行更快要更重要一些（至少开始是这样的）.
"""
