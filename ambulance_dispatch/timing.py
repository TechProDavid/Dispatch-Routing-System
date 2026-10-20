import time


def begin_timer():
    return time.perf_counter_ns()


def elapsed_nanoseconds(start_time):
    return time.perf_counter_ns() - start_time
