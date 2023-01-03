# -*- coding: utf-8 -*-

import functools


def perf_decorator(func):
    """A decorator to get details of function performance and intern calls."""
    import cProfile
    from io import StringIO
    from pstats import SortKey, Stats

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()
        value = func(*args, **kwargs)
        profile.disable()

        str_io = StringIO()
        profile_stats = Stats(profile, stream=str_io)

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
    from time import perf_counter_ns

    @functools.wraps(func)
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


def dircache_decorator(func):
    """A decorator to cache the result in disk."""
    import os
    import bz2
    import pickle
    from pathlib import Path
    from base64 import b64encode
    from uuid import uuid5, NAMESPACE_OID

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Create cache folder
        cache_root = Path(os.path.dirname(__file__), '__cache__')
        cache_root.mkdir(parents=True, exist_ok=True)

        # Checks if is already cached
        cache_key = (func.__code__.co_filename, func.__name__, args, kwargs)
        cache_name_raw = pickle.dumps(cache_key)
        cache_name_b64 = b64encode(cache_name_raw).decode('utf-8')
        cache_name = uuid5(NAMESPACE_OID, cache_name_b64).hex

        cache_file = Path(cache_root, cache_name).with_suffix('.bz2')
        if cache_file.exists():
            with bz2.open(cache_file, mode='rb') as file:
                value = pickle.load(file)
        else:
            value = func(*args, **kwargs)
            with bz2.open(cache_file, mode='wb') as file:
                pickle.dump(value, file)

        return value
    return wrapper
