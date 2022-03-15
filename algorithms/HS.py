import numpy as np
from solution import solution


class HS:
    def __init__(self, pars):
        self.NI = pars[[x[0] for x in pars].index('NI')][1]
        self.HMS = pars[[x[0] for x in pars].index('HMS')][1]
        self.HMCR = pars[[x[0] for x in pars].index('HMCR')][1]
        self.PAR = pars[[x[0] for x in pars].index('PAR')][1]
        self.BW = pars[[x[0] for x in pars].index('BW')][1]

    def evolve(self, f, d: int):
        self.function = f
        y = np.zeros(self.NI, float)
        self.best = solution(d, f)

        # Create the initial harmony memory and define the best solution
        harmony_memory = []
        for p in range(self.HMS):
            sol = solution(d, f)
            sol.Initialization([['mode', 1], ['number_of_scans', 0]])
            if p == 0:
                self.best.from_solution(sol)
            else:
                if sol.fitness < self.best.fitness:
                    self.best.from_solution(sol)
            y[p] = self.best.fitness
            harmony_memory.append(sol)
        harmony_memory.sort(key=lambda x: x.fitness)

        for iteration in range(self.HMS, self.NI):
            improvise = solution(d, f)
            for dim in range(d):
                if np.random.uniform() <= self.HMCR:
                    pos = int(np.random.uniform(0, self.HMS, 1)[0])
                    improvise.cells[dim] = harmony_memory[pos].cells[dim]
                    if np.random.uniform() <= self.PAR:
                        bandwidths = np.random.uniform(low=-self.BW, high=self.BW, size=1)
                        improvise.cells[dim] = improvise.cells[dim] + bandwidths
                else:
                    improvise.cells[dim] = np.random.uniform(low=f.lower_bound, high=f.upper_bound)
            improvise.cells[improvise.cells < f.lower_bound] = f.lower_bound
            improvise.cells[improvise.cells > f.upper_bound] = f.upper_bound
            improvise.fitness = f.evaluate(improvise.cells)

            if (improvise.fitness < harmony_memory[self.HMS - 1].fitness):
                harmony_memory[self.HMS - 1].from_solution(improvise)

            harmony_memory.sort(key=lambda x: x.fitness)

            if (harmony_memory[0].fitness < self.best.fitness):
                self.best.from_solution(harmony_memory[0])

            y[iteration] = self.best.fitness
        return y

    def __str__(self):
        result = "HS:HMS" + str(self.HMS) + "-HMCR:" + str(self.HMCR) + "-PAR" + str(self.PAR) + "-BW" + str(self.BW)
        return result
