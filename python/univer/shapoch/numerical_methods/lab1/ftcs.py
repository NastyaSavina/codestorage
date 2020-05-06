


from numpy.core import arange, linspace
import math as m
from matplotlib import pyplot as plt

def plot_ftcs(graph_index):
    def init_f(x):
        return 1.0

    def fi(x):
        return 1.0


    def fi_left(x, t):
        return 0


    def fi_right(x, t):
        return 0


    def f(x, t):
        return x ** 3 - 6 * x * t


    class FTCS_Solver(object):
        def __init__(self, t_start, t_end, l, tau, h, fi_func):
            self.t_start = t_end
            self.l = l
            self.tau = tau
            self.h = h
            self.fi_func = fi_func
            self.data = []

        def initialize(self, fi):
            init_arr = []
            for x in arange(0, self.l + self.h, self.h):
                init_arr.append(fi(x))
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
            
            
    def main():
        l = 1
        tau = 0.001
        h = 0.01

        t_arr_print = [0.0, 0.1, 0.5, 1.0, 5.0, 10.0]

        t_start = min(t_arr_print)
        t_end = max(t_arr_print) + tau

        d_start = 0.1
        d_end = 0.5
        d_step = 0.1


        x_arr = arange(h, l, h)
        t_arr = arange(t_start, t_end, tau)
        d_arr = arange(d_start, d_end + 0.0001, d_step)


        for d in d_arr:
            data = FTCS_Solver(t_start, t_end, l, tau, h, fi)
            data.initialize(init_f)

            for t in t_arr:
                data.set_u(
                    0, 
                    t + tau, 
                    d * (2 * data.u(h, t) - 2 * fi_left(0, t) - 2 * data.u(0, t)) \
                    + tau * f(0, t) \
                    + data.u(0, t)
                    )

                print(f"calculate for t: {round(t, 2)}")
                for x in x_arr:
                    data.set_u( 
                        x, 
                        t + tau, 
                        d * (data.u(x + h, t) + data.u(x - h, t) - 2 * data.u(x, t)) \
                        + tau * f(x, t) \
                        + data.u(x, t)
                        )

                data.set_u(
                    l, 
                    t + tau, 
                    d * (2 * data.u(l - h, t) - 2 * h * fi_right(l, t) - 2 * data.u(l, t)) \
                    + tau * f(l, t) \
                    + data.u(l, t)
                    )
                    
                if t in t_arr_print:
                    print(d)
                    print(t)
                    plt.figure(str(round(t, 2)))
                    plt.subplot(graph_index)
                    plt.plot([0, *x_arr, l], data.get_state(t))
                # for each in range(0, len(t_arr), round(len(t_arr) / 20)):
                #     plt.plot([0, *x_arr, l], data.get_state(t_arr[each]))


    main()
    
