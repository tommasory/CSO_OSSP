import numpy as np
import random
from solution import solution
from enum import Enum

class Behavior(Enum):
    SEEKING = 1
    TRACING = 2

class cat(solution):

    def __init__(self, d: int, f, behavior=None):
        super().__init__(d,f)
        self.behavior = behavior
        self.velocity = np.zeros(self.size, float)
        self.bestcells = np.zeros(self.size, float)
        self.bestfitness = 0.0

    def from_cat(self, origin):
        super().from_solution(origin)

        self.velocity = np.copy(origin.velocity)
        self.bestcells = np.copy(origin.bestcells)
        self.bestfitness = origin.bestfitness
        self.behavior = origin.behavior
        
    def Initialization(self):
        self.cells = np.random.uniform(low=self.function.lower_bound, high=self.function.upper_bound,size=(self.size,))
        
        self.fitness = self.function.evaluate(self.cells)

        self.velocity = np.random.uniform(low=-4, high=4,size=(self.size,))
        self.bestcells = np.copy(self.cells)
        self.bestfitness = self.fitness

    def move(self, c1, smp, srd, cdc, spc, best_cells):
        if self.behavior == Behavior.SEEKING:
            smp_cats = []

            """(1)	Make as many as SMP copies of the current position of Catk."""
            for _ in range(smp):
                c = cat(self.size,self.function)
                c.from_cat(self)
                smp_cats.append(c)

            if spc:
                smp_cats.pop()
                smp_cats.append(self)

            """
            (2)	For each copy, randomly select as many as CDC dimensions to be mutated. Moreover, randomly add or subtract SRD values from the current values, which replace the old positions as shown in the following equation:
            """

            for i in range(len(smp_cats)):
                cdc_dimensions = np.random.choice(self.size, size=cdc, replace=False)
                for dim in cdc_dimensions:
                    smp_cats[i].cells[dim] = (1 + random.random() + srd) * smp_cats[i].cells[dim]

            """ (3)	Evaluate the fitness value (FS) for all the candidate positions."""
            fitness_values = [self.function.evaluate(candidate.cells) for candidate in smp_cats]

            """
            (4)	Based on probability, select one of the candidate points to be the next position for the cat where candidate points with higher FS have more chance to be selected as shown in equation (2). However, if all fitness values are equal, then set all the selecting probability of each candidate point to be 1.
            """

            fit_max = max(fitness_values)
            fit_min = min(fitness_values)

            probabilities = [abs(value - fit_max) / (fit_max - fit_min) for value in fitness_values]

            prob_sum = sum(probabilities)

            probabilities = list(map(lambda prob: float(prob / prob_sum), probabilities))

            next_position_idx = np.random.choice(smp, 1, p = probabilities)[0]
            self.cells = smp_cats[next_position_idx].cells

        elif self.behavior == Behavior.TRACING:
            r1 = random.random()
            for dim in range(self.size):
                self.velocity[dim] = self.velocity[dim] + r1 * c1 * (best_cells[dim] - self.cells[dim])
                self.velocity[dim] = min(self.velocity[dim], self.function.upper_bound)
                self.velocity[dim] = max(self.velocity[dim], self.function.lower_bound)
                self.cells[dim] = self.cells[dim] + self.velocity[dim]
        else:
            raise Exception("Unreachable")

        self.fitness = self.function.evaluate(self.cells)

    def __str__(self):
        return "cells:" + str(self.cells) + \
               "-fit:" + str(self.fitness)
