class sphere:
    def __init__(self, lb: float, ub: float):
        self.lower_bound = lb
        self.upper_bound = ub
        self.optimum = 0.0

    @staticmethod
    def evaluate(cells):
        # sphere = x[0]^2 + x[1]^2 + x[2]^2 + ... + x[n-1]^2
        summa = (cells * cells).sum()
        return summa

    def __str__(self):
        return "Sphere-lb:" + str(self.lower_bound) + '-up:' + str(self.upper_bound)
