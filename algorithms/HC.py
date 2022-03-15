import numpy as np
from solution import solution


class HC:
    def __init__(self, pars):
        self.max_iterations = pars[[x[0] for x in pars].index('max_iterations')][1]
        self.mode = pars[[x[0] for x in pars].index('mode')][1]
        self.number_of_scans = 0
        self.bandwidth = 0
        self.standard_deviation = 0
        if self.mode == 1:
            self.bandwidth = pars[[x[0] for x in pars].index('bandwidth')][1]
        elif self.mode == 2:
            self.number_of_scans = pars[[x[0] for x in pars].index('number_of_scans')][1]
            self.standard_deviation = pars[[x[0] for x in pars].index('standard_deviation')][1]

    def evolve(self, f, d: int):
        self.function = f
        y = np.zeros(self.max_iterations, float)

        self.best = solution(d, f)
        self.best.Initialization([['mode', self.mode], ['number_of_scans', self.number_of_scans]])
        y[0:self.number_of_scans+1] = self.best.fitness

        S = self.best
        for iteration in range(self.number_of_scans+1, self.max_iterations):
            R = solution(S.size, S.function)
            R.from_solution(S)
            R.tweak([['mode', self.mode], ['bandwidth', self.bandwidth],
                    ['standard_deviation', self.standard_deviation]])
            if R.fitness < S.fitness:
                S.from_solution(R)
            y[iteration] = self.best.fitness
        return y

    def __str__(self):
        result = "HC-mode:" + str(self.mode)
        if self.mode == 1:
            result = result + "-bandwidth:" + str(self.bandwidth)
        elif self.mode == 2:
            result = "{0}-number_of_scans:{1}-standard_deviation:{2}".format(
                result, str(self.number_of_scans), str(self.standard_deviation))
        return result
