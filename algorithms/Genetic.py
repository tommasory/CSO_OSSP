import numpy as np
from solution import solution


class Genetic:
    def __init__(self, pars):
        self.max_iterations = pars[[x[0] for x in pars].index('max_iterations')][1]
        self.population_size = pars[[x[0] for x in pars].index('population_size')][1]
        self.bandwidth = pars[[x[0] for x in pars].index('bandwidth')][1]

    def evolve(self, f, d: int):
        self.function = f
        self.best = solution(d, f)
        y = np.zeros(self.max_iterations, float)

        # Create the initial population and define the best solution
        population = []
        for p in range(self.population_size):
            sol = solution(d, f)
            sol.Initialization([['mode', 1], ['number_of_scans', 0]])
            if p == 0:
                self.best.from_solution(sol)
            else:
                if sol.fitness < self.best.fitness:
                    self.best.from_solution(sol)
            y[p] = self.best.fitness
            population.append(sol)

        max_generations = int(self.max_iterations / self.population_size)

        for generation in range(1, max_generations):
            offspring = []
            for s in range(self.population_size):
                # Parent selection operation using choice function to avoid the while seen in class
                # In this case, random parent selection drives exploration (diversity)
                options = np.random.choice(self.population_size, size=2, replace=False)
                p1 = options[0]
                p2 = options[1]

                # Crossover operation
                # One point crossover drives exploitation
                song = solution(d, f)
                song.crossover(population[p1], population[p2])

                # Mutation operation
                # In this case, one-bit mutation with low bandwidth drives exploitation
                song.uniform_tweak_one_gen(self.bandwidth)

                if song.fitness < self.best.fitness:
                    self.best.from_solution(song)
                y[s + generation * self.population_size] = self.best.fitness

                # Who goes to the new population?
                # In this case, all offspring goes to the population then we are going to
                # select the best solutions from current and previous population
                offspring.append(song)

            # Population replacement operation
            # In this case, eliminate the worst solutions from the two populations
            # (current and new), this operation drives exploitation of best solutions found
            population = population + offspring
            population.sort(key=lambda x: x.fitness)
            del population[self.population_size: self.population_size + self.population_size]

        return y

    def __str__(self):
        result = "Genetic-population_size:" + str(self.population_size) + \
                 "-bandwidth:" + str(self.bandwidth)
        return result
