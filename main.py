import numpy as np
from algorithms.CSO import CSO
from diff_time import diff_time
from functions.sphere import sphere

if __name__ == '__main__':

    my_sphere = sphere(-5.0, 5.0)
    max_iterations = 1000
    dimensions = 15
    max_repetitions = 31

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

    x = np.arange(max_iterations)
    curve = []
    pos = 0
    print("{0:30}".format(str(my_sphere)), end=" ")
    curve.append(np.zeros(max_iterations, float))
    best = np.zeros(max_repetitions, dtype=float)
    my_time = diff_time()
    for this_repetition in range(max_repetitions):
        np.random.seed(this_repetition)
        curve[pos] = curve[pos] + my_cso.evolve(my_sphere, dimensions)
        best[this_repetition] = my_cso.best.fitness

    
    print("{0:20}".format(str(my_cso)) +
            " {0:12.6f}".format(best.mean()) + " {0:12.6f}".format(best.std()) +
            " {0:12.6f}".format(best.max()) + " {0:12.6f}".format(best.min()) +
            " {0:10.5f}".format(my_time.end() / max_repetitions), end=" ")
    for cells in my_cso.best.cells:
        print(cells)

