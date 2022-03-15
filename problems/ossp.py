import numpy as np
from pathlib import Path


class ossp:
    size: int

    def __init__(self, filename):
        file1 = open(filename, 'r')
        lines = file1.readlines()

        jobs  = int(lines[0])
        self.work_list = []
        flag = 1
        for pos in range(1, jobs+1):
            str_line = lines[pos].replace('\n','')
            line = [int(e) for e in str_line.split(',')]
            job = line.pop(0)
            #line = self.pair_list(line)
            for i in range(len(line)):
                if i%2:
                    aux = [flag, job, line[i-1], line[i]]
                    self.work_list.append(aux)
                    flag += 1
        self.size = len(self.work_list)

    def evaluate(self, cells):
        fitness = 0
        for i in range(self.size):
            j = i + 1
            if j >= self.size:
                j = 0
            fitness = fitness + self.distances[cells[i]][cells[j]]
        return fitness

    def __str__(self):
        return Path(self.file_name).stem