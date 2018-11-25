import time

class MyTimer:

    _start_time = 0

    def __init__(self):
        self._start_time = time.time()

    def execTime(self):
        return time.time() - self._start_time

    