import numpy as np


class step:
    def __init__(self, lb: float, ub: float):
        self.lower_bound = lb
        self.upper_bound = ub
        self.optimum = 0.0

    @staticmethod
    def evaluate(cells):
        new_cells = np.floor(cells + 0.5)
        summa = (new_cells * new_cells).sum()
        return summa

    def __str__(self):
        return "Step-lb:" + str(self.lower_bound) + '-up:' + str(self.upper_bound)
