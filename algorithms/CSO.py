import random
import numpy as np
from cat import *
from solution import solution


class CSO:
    def __init__(self, pars):
        self.max_efos = pars[[x[0] for x in pars].index('max_efos')][1]
        self.swarm_size = pars[[x[0] for x in pars].index('n')][1]
        self.smp = pars[[x[0] for x in pars].index('smp')][1] 
        self.spc = pars[[x[0] for x in pars].index('spc')][1]
        self.srd = pars[[x[0] for x in pars].index('srd')][1]
        self.cdc = pars[[x[0] for x in pars].index('cdc')][1]
        self.mr = pars[[x[0] for x in pars].index('mr')][1]
        self.max_velocity = 1

    def evolve(self, f, d: int):
        y = np.zeros(self.max_efos, float)
        self.best = cat(d, f)
        behavior_pattern = self.generate_behavior()

        # Create the initial swarm and define the best solution
        swarm = []
        for p in range(self.swarm_size):
            mycat = cat(d, f, behavior_pattern[p])
            mycat.Initialization()
            if p == 0:
                self.best.from_cat(mycat)
            else:
                if mycat.fitness < self.best.fitness:
                    self.best.from_cat(mycat)
            y[p] = self.best.fitness
            swarm.append(mycat)
        swarm.sort(key=lambda x: x.fitness)
        swarm[0].behavior = Behavior.SEEKING

        #fly over the search space
        max_steps = int(self.max_efos / self.swarm_size)
        count = self.swarm_size
        for steps in range(1, max_steps):
            for p in range(self.swarm_size):
                swarm[p].move(self.smp, self.srd, self.cdc, self.spc, self.max_velocity, self.best.cells)
                if swarm[p].fitness < self.best.fitness:
                    self.best.from_cat(swarm[p])
                y[count] = self.best.fitness
                count += 1
                
            behavior_pattern = self.generate_behavior()
            for p in range(self.swarm_size):
                swarm[p].behavior = behavior_pattern[p]

        return y

    def generate_behavior(self):
        behavior_pattern = [Behavior.TRACING] * self.swarm_size
        for _ in range(self.swarm_size):
            sm = random.random() < self.mr
            if sm:
                behavior_pattern[random.randint(0, self.swarm_size-1)] = Behavior.SEEKING
        return behavior_pattern

    def __str__(self):
        result = "CSO:swarm_size:" + str(self.swarm_size)
        return result
