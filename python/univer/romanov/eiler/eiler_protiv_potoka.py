def init_f(x, x0):
    return m.exp(-(x - x0) ** 2)


def fi_left(x, t):
    return 0


def fi_right(x, t):
    return 0


def f(x, t):
    # return x ** 3 - 6 * x * t
    return 0

from numpy.core import arange, linspace
import math as m
from matplotlib import pyplot as plt
import matplotlib.animation as ani


class FTCS_Solver(object):
    def __init__(self, t_start, t_end, l, tau, h, x0):
        self.t_start = t_end
        self.l = l
        self.tau = tau
        self.h = h
        self.data = []
        self.x0 = x0

    def initialize(self, f):
        init_arr = []
        for x in arange(0, self.l + self.h, self.h):
            init_arr.append(f(x, self.x0))
        self.data.append(init_arr)

    def u(self, x, t):
        i = int(round(t / self.tau))
        j = int(round(x / self.h))

        # print()
        # print()
        # print()
        # print()
        # print(x)
        # print(t)
        # print(i)
        # print(j)
        # print(len(self.data))
        # print(len(self.data[i]))
        # print(self.data)
        # print(self.data[i])
        
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
        
        
if __name__ == "__main__": 
    l = 200

    x0 = l / 2
    tau = 0.005
    h = 0.1

    t_arr_print = [0.0, 0.1, 0.5, 1.0, 2.05]

    t_start = min(t_arr_print)
    t_end = max(t_arr_print) + tau

    d_start = 0.0
    d_end = 0.0
    d_step = 0.1

    c = 1

    x_arr = arange(h, l, h)
    t_arr = arange(t_start, t_end, tau)
    d_arr = arange(d_start, d_end + 0.0001, d_step)


    for d in d_arr:
        data = FTCS_Solver(t_start, t_end, l, tau, h, x0)
        data.initialize(init_f)

        for t in t_arr:
            data.set_u(0, t + tau, 0)

            print(f"calculate for t: {round(t, 2)}")
            for x in x_arr:
                data.set_u( 
                    x, 
                    t + tau, 
                    data.u(x, t) - c * tau / h * (data.u(x, t) - data.u(x - h, t))
                    )

            data.set_u(l, t + tau, 0)

    
    fig = plt.figure()
    ax = plt.axes()

    def animate(n):
        global ax
        global fig
        global data
        global l
        global h

        hist = data.data
        print(hist[n])
        x_range = arange(0, l + h, h)
        ax.clear()
        ax.plot(x_range, hist[n])
        return x_range,


    _a_ = ani.FuncAnimation(fig, 
            animate, 
            frames=len(data.data), 
            interval=1, 
            repeat=False)

    plt.show()
