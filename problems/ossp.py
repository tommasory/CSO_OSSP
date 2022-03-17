import numpy as np

class ossp:
    size: int

    def __init__(self, filename):
        file1 = open(filename, 'r')
        lines = file1.readlines()

        jobs  = int(lines[0])
        self.operations = []
        flag = 1
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

    def evaluate(self, cells: 'list(int)'):
        schedule = Schedule(cells, self.operations)
        end_time = schedule.getEndTime()
        return end_time

class Operation:
    def __init__(self, element):
        self.number = element[0] 
        self.job = element[1]
        self.machine = element[2] 
        self.time = element[3] 

    def __repr__(self):
        return "<Operation number %s: job:%s, machine:%s, time:%s>" % (self.number, self.job, self.machine, self.time)

class Schedule:
    def __init__(self, sequence, operations):
        self.sequence = sequence
        self.operations = operations
        self.jobs_next_free_time = {}
        self.machines_schedule = {}

        self.buildMachinesSchedule()

    def buildMachinesSchedule(self):
        for op_index in self.sequence:
            # Find job and machine free times
            op = [op for op in self.operations if op.number == op_index][0]
            
            job_next_free_time = 0
            if op.job in self.jobs_next_free_time:
                job_next_free_time = self.jobs_next_free_time[op.job]
                
            machine_next_free_time = self.findMachineAvailableTime(op.machine, job_next_free_time, op.time)

            # Reconcile op start time 
            op_start_time = max(job_next_free_time, machine_next_free_time)

            self.jobs_next_free_time[op.job] = op_start_time

            # Add op event to machine schedule
            if op.machine not in self.machines_schedule:
                self.machines_schedule[op.machine] = []

            self.machines_schedule[op.machine].append((op_start_time, op_start_time+op.time))
            self.machines_schedule[op.machine].sort(key=lambda event: event[0])

    def findMachineAvailableTime(self, machine:int, min_start: int, duration: int) -> int:
        # If nothing scheduled, return 0
        if machine not in self.machines_schedule:
            return 0

        schedule = self.machines_schedule[machine]

        for i, event in enumerate(schedule):
            # If it's the last event, return the event end time
            if i+1 == len(schedule):
                return event[1]

            next_event = schedule[i+1]

            # If the incoming event fits, return the machine event end time
            if event[1] >= min_start and next_event[0] <= min_start+duration:
                return event[1]
    
    def getEndTime(self):
        max_end_time = 0
        for machine in self.machines_schedule:
            schedule = self.machines_schedule[machine]

            if len(schedule) == 0:
                continue

            last_event = schedule[-1]
            if last_event[1] > max_end_time:
                max_end_time = last_event[1]

        return max_end_time