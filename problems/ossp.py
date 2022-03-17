import numpy as np

class ossp:
    size: int

    def __init__(self, filename):
        file1 = open(filename, 'r')
        lines = file1.readlines()

        jobs  = int(lines[0])
        self.operations = []
        flag = 0
        for pos in range(1, jobs+1):
            str_line = lines[pos].replace('\n','')
            line = [int(e) for e in str_line.split(',')]
            job = line.pop(0)
            #line = self.pair_list(line)
            for i in range(len(line)):
                if i%2:
                    aux = [flag, job, line[i-1], line[i]]
                    self.operations.append(Operation(aux))
                    flag += 1
        self.size = len(self.operations)

    def evaluate(self, cells):
        fitness = 0
        return np.random.randint(100)

class Operation:
    def __init__(self, element):
        self.number = element[0] 
        self.job = element[1] 
        self.machine = element[2] 
        self.time = element[3] 

    def __repr__(self):
        return "<Operation number %s: job:%s, machine:%s, time:%s>" % (self.number, self.job, self.machine, self.time)