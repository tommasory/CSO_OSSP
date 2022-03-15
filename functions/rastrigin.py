import numpy as np


class rastrigin:
    def __init__(self, lb: float, ub: float):
        self.lower_bound = lb
        self.upper_bound = ub
        self.optimum = 0.0

    @staticmethod
    def evaluate(cells):
        summa = (np.power(cells, 2) - 10 * np.cos(2 * np.pi * cells) + 10).sum()
        return summa

    def __str__(self):
        return "Rastrigin-lb:" + str(self.lower_bound) + '-up:' + str(self.upper_bound)
