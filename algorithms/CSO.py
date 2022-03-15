import random
import numpy as np
from cat import *
from solution import solution


class CSO:
    def __init__(self, pars):
        self.max_efos = pars[[x[0] for x in pars].index('max_efos')][1]
        self.swarm_size = pars[[x[0] for x in pars].index('swarm_size')][1]
        self.C1 = pars[[x[0] for x in pars].index('c1')][1]
        self.SMP = pars[[x[0] for x in pars].index('SMP')][1] 
        self.SRD = pars[[x[0] for x in pars].index('SRD')][1]
        self.CDC = pars[[x[0] for x in pars].index('CDC')][1]
        self.SPC = pars[[x[0] for x in pars].index('SPC')][1]
        self.MR = pars[[x[0] for x in pars].index('mr')][1]

    def evolve(self, f, d: int):
        self.function = f
        y = np.zeros(self.max_efos, float)
        self.best = cat(d, f)
        num_seeking = int(((self.MR * self.swarm_size) / self.swarm_size*2))
        behavior_pattern = self.generate_behavior(num_seeking)

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
                swarm[p].move(self.C1, self.SMP, self.SRD, self.CDC, self.SPC, self.best.cells)
                if swarm[p].fitness < self.best.fitness:
                    self.best.from_cat(swarm[p])
                y[count] = self.best.fitness
                count += 1
                
            behavior_pattern = self.generate_behavior(num_seeking)
            for p in range(self.swarm_size):
                swarm[p].behavior = behavior_pattern[p]

        return y

    def generate_behavior(self, num_seeking):
        behavior_pattern = [Behavior.TRACING] * self.swarm_size
        for _ in range(num_seeking):
            behavior_pattern[random.randint(0, self.swarm_size-1)] = Behavior.SEEKING
        return behavior_pattern

    def __str__(self):
        result = "CSO:swarm_size:" + str(self.swarm_size)
        return result
