import time


class diff_time:

    def __init__(self):
        self.t1 = time.monotonic()

    def end(self):
        t2 = time.monotonic()
        return t2 - self.t1
