import numpy as np
import matplotlib.pyplot as plt

from algorithms.Genetic import Genetic
from algorithms.HS import HS
from algorithms.PSO import PSO
from algorithms.CSO import CSO
from diff_time import diff_time
from algorithms.HC import HC
from algorithms.SAHC import SAHC
from functions.ackley import ackley
from functions.griewank import griewank
from functions.sphere import sphere
from functions.step import step
from functions.schwefel import schwefel
from functions.rastrigin import rastrigin

if __name__ == '__main__':

    my_step = step(-5.0, 5.0)
    my_sphere = sphere(-5.0, 5.0)
    my_schwefel = schwefel(-100, 100)
    my_rastrigin = rastrigin(-5.12, 5.12)
    my_griewank = griewank(-600, 600)
    my_functions = [my_sphere, my_step, my_schwefel, my_rastrigin,my_griewank]

    max_iterations = 1000
    dimensions = 15
    max_repetitions = 31

    my_hc = HC([['max_iterations', max_iterations], ['mode', 1], ['bandwidth', 0.8],
                ['number_of_scans', 0], ['standard_deviation', 0.8]])
    my_hc2 = HC([['max_iterations', max_iterations], ['mode', 2], ['bandwidth', 0.8],
                  ['number_of_scans', 10], ['standard_deviation', 0.8]])
    my_sahc = SAHC([['max_iterations', max_iterations], ['times', 10],
                  ['mode', 1], ['bandwidth', 0.8],
                  ['number_of_scans', 10], ['standard_deviation', 0.8]])
    my_genetic = Genetic([['max_iterations', max_iterations], ['population_size', 20],
                          ['bandwidth', 0.8]])
    my_hs = HS([['NI', max_iterations], ['HMS', 20], ['HMCR', 0.85],
                ['PAR', 0.3], ['BW', 0.9]])
    my_pso = PSO([['max_efos', max_iterations], ['swarm_size', 20],
                  ['alfa', 0.3], ['beta', 0.2], ['delta', 0.5], ['epsilon', 1]])

    my_cso = CSO([
        ['max_efos', max_iterations], 
        ['swarm_size', 20],
        ['c1',2],
        ['SMP',3],
        ['SRD',2],
        ['CDC',3],
        ['SPC',True],
        ['mr',2]
    ])

    my_algorithms = [my_cso,my_pso, my_hs, my_genetic, my_hc , my_sahc]

    for my_function in my_functions:
        x = np.arange(max_iterations)
        curve = []
        pos = 0
        print("{0:30}".format(str(my_function)), end=" ")
        for my_algorithm in my_algorithms:
            curve.append(np.zeros(max_iterations, float))
            best = np.zeros(max_repetitions, dtype=float)
            my_time = diff_time()
            for this_repetition in range(max_repetitions):
                np.random.seed(this_repetition)
                curve[pos] = curve[pos] + my_algorithm.evolve(my_function, dimensions)
                best[this_repetition] = my_algorithm.best.fitness

            print("{0:20}".format(str(my_algorithm)) +
                  " {0:12.6f}".format(best.mean()) + " {0:12.6f}".format(best.std()) +
                  " {0:12.6f}".format(best.max()) + " {0:12.6f}".format(best.min()) +
                  " {0:10.5f}".format(my_time.end() / max_repetitions), end=" ")
            curve[pos] = curve[pos] / max_repetitions
            pos = pos + 1

        print("")
        # plotting
        plt.title("Convergence curve for " + str(my_function))
        plt.xlabel("Iteration")
        plt.ylabel("Fitness")
        leg = []
        for i in range(len(my_algorithms)):
            plt.plot(x, curve[i])
            leg.append(str(my_algorithms[i]))
        plt.legend(leg)
        plt.show()
