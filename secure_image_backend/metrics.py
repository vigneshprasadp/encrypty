import time

def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        t = time.time() - start
        return result, round(t, 4)
    return wrapper
