from numpy.core import arange

class FTCS_Solver(object):
    def __init__(self, t_start, t_end, l, tau, h, fi_func):
        self.t_start = t_end
        self.l = l
        self.tau = tau
        self.h = h
        self.fi_func = fi_func
        self.data = []

    def initialize(self, init_f):
        init_arr = []
        for x in arange(0, self.l + self.h, self.h):
            init_arr.append(init_f(x, self.h))
        self.data.append(init_arr)

    def u(self, x, t):
        i = int(round(t / self.tau))
        j = int(round(x / self.h))
        
        return self.data[i][j]

    def add_line(self, line):
        self.data.append(line)

    def set_u(self, x, t, value):
        i = int(round(t / self.tau))
        j = int(round(x / self.h))
        
        if len(self.data) > i and len(self.data[i]) > j:
            self.data[i][j] = value
        elif len(self.data) <= i:
            self.data.append([value])
        elif len(self.data[i]) <= j:
            self.data[i].append(value)

    def get_state(self, t):
        i = int(round(t / self.tau))
        return self.data[i]
        
        