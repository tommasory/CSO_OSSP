import math

import numpy as np


class ackley:
    def __init__(self, lb: float, ub: float):
        self.lower_bound = lb
        self.upper_bound = ub
        self.optimum = 0.0

    @staticmethod
    def evaluate(cells):
        t1 = -0.2 * math.sqrt((np.power(cells, 2)).sum() / len(cells))
        t2 = math.exp((np.cos(2 * np.pi * cells)).sum() / len(cells))
        return -20 * math.exp(t1 - t2) + 20 + math.exp(1)

    def __str__(self):
        return "Ackley-lb:" + str(self.lower_bound) + '-up:' + str(self.upper_bound)
