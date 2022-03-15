import numpy as np


class solution:

    def __init__(self, d: int, f):
        self.size = d
        self.cells = np.zeros(self.size, float)
        self.fitness = 0.0
        self.function = f

    def from_solution(self, origin):
        self.size = origin.size
        self.cells = np.copy(origin.cells)
        self.fitness = origin.fitness
        self.function = origin.function

    def Initialization(self, pars):
        mode = pars[[x[0] for x in pars].index('mode')][1]
        if mode == 1:
            return self.randomInitialization1()
        elif mode == 2:
            number_of_scans = pars[[x[0] for x in pars].index('number_of_scans')][1]
            return self.randomInitialization2(number_of_scans)

    def randomInitialization1(self):
        self.cells = np.random.uniform(low=self.function.lower_bound, high=self.function.upper_bound,
                                       size=(self.size,))
        self.fitness = self.function.evaluate(self.cells)

    def randomInitialization2(self, number_of_scans: int):
        for i in range(number_of_scans):
            this_cells = np.random.uniform(low=self.function.lower_bound,
                                           high=self.function.upper_bound, size=(self.size,))
            this_fitness = self.function.evaluate(this_cells)
            if i == 1:
                self.cells = np.copy(this_cells)
                self.fitness = this_fitness
            if this_fitness < self.fitness:
                self.cells = np.copy(this_cells)
                self.fitness = this_fitness

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
