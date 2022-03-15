class schwefel:
    def __init__(self, lb: float, ub: float):
        self.lower_bound = lb
        self.upper_bound = ub
        self.optimum = 0.0

    @staticmethod
    def evaluate(cells):
        summa = 0
        for i in range(len(cells) + 1):
            summa = summa + pow(cells[:i].sum(), 2)
        return summa

    def __str__(self):
        return "Schwefel-lb:" + str(self.lower_bound) + '-up:' + str(self.upper_bound)
