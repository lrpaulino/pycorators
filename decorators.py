# -*- coding: utf-8 -*-

import cProfile
import pstats

from datetime import datetime
from functools import wraps
from io import StringIO
from pstats import SortKey
from time import perf_counter_ns


def perf_decorator(func):
    """A decorator to get details of function performance and intern calls."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()
        value = func(*args, **kwargs)
        profile.disable()

        str_io = StringIO()
        profile_stats = pstats.Stats(profile, stream=str_io)

        sort_by = SortKey.CUMULATIVE
        profile_stats = profile_stats.sort_stats(sort_by)
        profile_stats = profile_stats.reverse_order()
        profile_stats.print_stats(50)

        print('Function:', func.__name__)
        print(str_io.getvalue())

        return value
    return wrapper


def time_decorator(func):
    """A decorator to get the elapsed time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter_ns()
        value = func(*args, **kwargs)
        end = perf_counter_ns()

        elapsed_time = end - start

        print('Function:', func.__name__, end=', ')
        print('elapsed time:', end=' ')
        if elapsed_time < 10**3:
            print(elapsed_time, 'ns')
        elif elapsed_time < 10**6:
            print(elapsed_time / 10**3, 'us')
        elif elapsed_time < 10**9:
            print(elapsed_time / 10**6, 'ms')
        elif elapsed_time < 6*10**10:
            print(elapsed_time / 10**9, 's')
        else:
            seconds = elapsed_time / 10**9
            minutes = int(seconds // 60)
            seconds -= minutes * 60
            print(minutes, 'min and',
                  seconds, 's')

        return value
    return wrapper


def try_except_decorator(func):
    pass
