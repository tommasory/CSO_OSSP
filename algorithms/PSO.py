import numpy as np

from particle import particle
from solution import solution


class PSO:
    def __init__(self, pars):
        self.max_efos = pars[[x[0] for x in pars].index('max_efos')][1]
        self.swarm_size = pars[[x[0] for x in pars].index('swarm_size')][1]
        self.alfa = pars[[x[0] for x in pars].index('alfa')][1]
        self.beta = pars[[x[0] for x in pars].index('beta')][1]
        self.delta = pars[[x[0] for x in pars].index('delta')][1]
        self.epsilon = pars[[x[0] for x in pars].index('epsilon')][1]

    def evolve(self, f, d: int):
        self.function = f
        y = np.zeros(self.max_efos, float)
        self.best = particle(d, f)

        # Create the initial swarm and define the best solution
        swarm = []
        for p in range(self.swarm_size):
            myparticle = particle(d, f)
            myparticle.Initialization()
            if p == 0:
                self.best.from_particle(myparticle)
            else:
                if myparticle.fitness < self.best.fitness:
                    self.best.from_particle(myparticle)
            y[p] = self.best.fitness
            swarm.append(myparticle)
        swarm.sort(key=lambda x: x.fitness)

        #fly over the search space
        max_steps = int(self.max_efos / self.swarm_size)
        count = self.swarm_size
        for steps in range(1, max_steps):
            for p in range(self.swarm_size):
                for dim in range(d):
                    my_beta = np.random.uniform(low=0, high=self.beta,size=1)[0]
                    my_delta = np.random.uniform(low=0, high=self.delta, size=1)[0]

                    swarm[p].velocity[dim] = self.alfa * swarm[p].velocity[dim] + \
                                             my_beta * (swarm[p].bestcells[dim] - swarm[p].cells[dim]) + \
                                             my_delta * (self.best.cells[dim] - swarm[p].cells[dim])

                swarm[p].cells = swarm[p].cells + self.epsilon * swarm[p].velocity

                swarm[p].cells[swarm[p].cells < self.function.lower_bound] = self.function.lower_bound
                swarm[p].cells[swarm[p].cells > self.function.upper_bound] = self.function.upper_bound

                swarm[p].fitness = self.function.evaluate(swarm[p].cells)

                if swarm[p].fitness < self.best.fitness:
                    self.best.from_particle(swarm[p])
                y[count] = self.best.fitness
                count += 1

        return y

    def __str__(self):
        result = "PSO:swarm_size:" + str(self.swarm_size)
        return result
