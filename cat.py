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
        self.velocity = 1
        self.bestcells = np.zeros(self.size, float)
        self.bestfitness = 0.0

    def from_cat(self, origin):
        super().from_solution(origin)
        self.velocity = origin.velocity
        self.bestcells = np.copy(origin.bestcells)
        self.bestfitness = origin.bestfitness
        self.behavior = origin.behavior
        
    def Initialization(self):
        self.cells = np.random.choice(self.size, self.size, replace=False)
        self.fitness = self.function.evaluate(self.cells)
        self.velocity = 1
        self.bestcells = np.copy(self.cells)
        self.bestfitness = self.fitness

    def mutate(self, cells, cdc):
        srd = np.random.choice(self.size-1, 1, replace=False)
        borders = []
        borders.append(srd)
        borders.append((cdc + srd) % self.size)
        borders.sort()

        mid = int((borders[1]-borders[0])/2)
        # Switch values between borders
        for i in range(mid+1):
            tmp = cells[borders[0]+i]
            cells[borders[0]+i] = cells[borders[1]-i]
            cells[borders[1]-i] = tmp
        return cells

    def move(self, smp, srd, cdc, spc, max_velocity, best_cells):
        if self.behavior == Behavior.SEEKING:
            candidates = []

            """(1)	Make as many as SMP copies of the current position of Catk."""
            for _ in range(smp):
                c = cat(self.size,self.function)
                c.from_cat(self)
                candidates.append(c)

            if spc:
                candidates.pop()
                candidates.append(self)

            """
            (2)	For each copy, randomly select as many as CDC dimensions to be mutated. Moreover, randomly add or subtract SRD values from the current values, which replace the old positions as shown in the following equation:
            """

            for i in range(len(candidates)):
                candidates[i].cells = self.mutate(candidates[i].cells, cdc)

            """ (3)	Evaluate the fitness value (FS) for all the candidate positions."""
            fitness_values = [self.function.evaluate(candidate.cells) for candidate in candidates]

            """
            (4)	Based on probability, select one of the candidate points to be the next position for the cat where candidate points with higher FS have more chance to be selected as shown in equation (2). However, if all fitness values are equal, then set all the selecting probability of each candidate point to be 1.
            """

            fit_max = max(fitness_values)
            fit_min = min(fitness_values)

            probabilities = [abs(value - fit_max) / (fit_max - fit_min) for value in fitness_values]

            prob_sum = sum(probabilities)

            probabilities = list(map(lambda prob: float(prob / prob_sum), probabilities))

            next_position_idx = np.random.choice(smp, 1, p = probabilities)[0]
            self.cells = candidates[next_position_idx].cells

        elif self.behavior == Behavior.TRACING:
            w = 0.7
            r = random.random()
            c = 2.05
            for pos in range(self.size):
                self.velocity = w * self.velocity + r * c * (best_cells[pos] - self.cells[pos])
                self.velocity = np.where(self.velocity > max_velocity, self.velocity, max_velocity)
                self.cells[pos] = (self.cells[pos] + int(self.velocity)) % self.size

                if self.cells[pos] == 0:
                    self.cells[pos] = 1
            self.fitness = self.function.evaluate(self.cells)

        else:
            raise Exception("Unreachable")

        self.fitness = self.function.evaluate(self.cells)

    def __str__(self):
        return "cells:" + str(self.cells) + \
               "-fit:" + str(self.fitness)
