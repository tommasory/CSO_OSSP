import numpy as np
from solution import solution


class particle (solution):

    def __init__(self, d: int, f):
        super().__init__(d,f)

        self.velocity = np.zeros(self.size, float)
        self.bestcells = np.zeros(self.size, float)
        self.bestfitness = 0.0

    def from_particle(self, origin):
        super().from_solution(origin)

        self.velocity = np.copy(origin.velocity)
        self.bestcells = np.copy(origin.bestcells)
        self.bestfitness = origin.bestfitness
        
    def Initialization(self):
        self.cells = np.random.uniform(low=self.function.lower_bound, high=self.function.upper_bound,size=(self.size,))
        
        self.fitness = self.function.evaluate(self.cells)

        self.velocity = np.random.uniform(low=-4, high=4,size=(self.size,))
        self.bestcells = np.copy(self.cells)
        self.bestfitness = self.fitness

    def tweak(self, pars):
        mode = pars[[x[0] for x in pars].index('mode')][1]
        if mode == 1:
            bandwidth = pars[[x[0] for x in pars].index('bandwidth')][1]
            return self.uniform_tweak(bandwidth)
        elif mode == 2:
            standard_deviation = pars[[x[0] for x in pars].index('standard_deviation')][1]
            return self.normal_tweak(standard_deviation)

    def uniform_tweak(self, bandwidth: float):
        bandwidths = np.random.uniform(low=-bandwidth, high=bandwidth, size=(self.size,))
        self.cells = self.cells + bandwidths
        self.cells[self.cells < self.function.lower_bound] = self.function.lower_bound
        self.cells[self.cells > self.function.upper_bound] = self.function.upper_bound
        self.fitness = self.function.evaluate(self.cells)

    def normal_tweak(self, standard_deviation: float):
        variations = np.random.normal(loc=0, scale=standard_deviation, size=(self.size,))
        self.cells = self.cells + variations
        self.cells[self.cells < self.function.lower_bound] = self.function.lower_bound
        self.cells[self.cells > self.function.upper_bound] = self.function.upper_bound
        self.fitness = self.function.evaluate(self.cells)

    def crossover(self, parent1, parent2):
        point = np.random.randint(parent1.size - 1, size=1, dtype=int)[0]
        self.cells[0:point + 1] = parent1.cells[0:point + 1]
        self.cells[point + 1:] = parent2.cells[point + 1:]

    def uniform_tweak_one_gen(self, bandwidth: float):
        point = np.random.randint(self.size, size=1, dtype=int)[0]
        self.cells[point] = self.cells[point] + np.random.uniform(low=-bandwidth, high=bandwidth, size=1)[0]
        self.cells[self.cells < self.function.lower_bound] = self.function.lower_bound
        self.cells[self.cells > self.function.upper_bound] = self.function.upper_bound
        self.fitness = self.function.evaluate(self.cells)

    def __str__(self):
        return "cells:" + str(self.cells) + \
               "-fit:" + str(self.fitness)
