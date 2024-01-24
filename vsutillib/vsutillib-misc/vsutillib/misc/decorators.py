"""
Decorators found on internet
"""


from functools import wraps
from time import time


def callCounter(func):
    """function call counter"""

    @wraps(func)
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0

    return helper


def staticVars(**kwargs):
    """Add static variables to function"""

    def decorate(func):
        """Add attributes to func"""
        for (k, v) in kwargs.items():
            setattr(func, k, v)
        return func
    return decorate


def timing(func):
    """function timing"""
    @wraps(func)
    def wrap(*args, **kwargs):

        timeStart = time()
        result = func(*args, **kwargs)
        timeStop = time()

        print(
            f"func:{func.__name__} args:[{args}, {kwargs}] "
            f"took: {(timeStart - timeStop):.4f}")

        return result
    return wrap
