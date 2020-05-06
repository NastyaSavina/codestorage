from numpy.core import arange, linspace
import math as m
from matplotlib import pyplot as plt

def plot_df(graph_index):

    print("found")
    def init_f(x):
        return -1.0

    def fi(x):
        return 1.0


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

        def initialize(self, f):
            init_arr = []
            for x in arange(0, self.l + self.h, self.h):
                init_arr.append(f(x))
            self.data.append(init_arr)

        def u(self, x, t):
            i = int(round(t / self.tau))
            j = int(round(x / self.h))

            return self.data[i][j]

        def add_line(self, line):
            self.data.append(line)

        def set_u(self, x_, t_, value):
            i_ = int(round(t_ / self.tau))
            j_ = int(round(x_ / self.h))
            
            
            if len(self.data) > i_ and len(self.data[i_]) > j_:
                self.data[i_][j_] = value
                
            elif len(self.data[i_]) <= j_:
                self.data[i_].append(value)


        def get_state(self, t):
            i = int(round(t / self.tau))
            return self.data[i]
            
            

    def main():
        l = 1
        tau = 0.05
        h = 0.05

        t_arr_print = [0.0, 0.1, 0.5, 1.0, 5.0, 10.0]

        t_start = min(t_arr_print)
        t_end = max(t_arr_print) + tau

        d_start = 0.0
        d_end = 2.5
        d_step = 0.1


        t_arr = arange(t_start + tau, t_end, tau)
        d_arr = [0.1, 0.5, 0.6, 2.5] 


        for d in d_arr:
            x_arr = arange(h, l, h)
            data = FTCS_Solver(t_start, t_end, l, tau, h, fi)
            data.initialize(init_f)
            data.initialize(init_f)

            for t in t_arr:
                empty_line = []
                for i in range(int(l / h)):
                    empty_line.append(0)
                data.add_line(empty_line)
                data.set_u(
                    0, 
                    t + tau, 
                    (2 * d * (data.u(0 + h, t) 
                            - data.u(0, t - tau) 
                            + data.u(0 + h, t)) 
                    + 2 * tau * f(0, t)
                    + data.u(0, t - tau)) / (1 + 2 * d)
                    )
                data.set_u(l, t + tau, 
                        (2 * d * (data.u(l - h, t)
                                - data.u(l, t - tau) 
                                + data.u(l - h, t)) 
                        + 2 * tau * f(l, t)
                        + data.u(l, t - tau)) / (1 + 2 * d)
                        )

                for x in x_arr:
                    print(f"calculate for d: {round(d, 1)} t: {round(t, 2)} x: {round(x, 2)}")
                    data.set_u( 
                        x, 
                        t + tau, 
                        (2 * d * (data.u(x + h, t) 
                                - data.u(x, t - tau) 
                                + data.u(x - h, t)) 
                        + 2 * tau * f(x, t)
                        + data.u(x, t - tau)) / (1 + 2 * d)
                        )
                    
                if round(t, 5) in t_arr_print:
                    plt.figure(str(round(t, 2)))
                    plt.subplot(graph_index)
                    plt.plot([0, *x_arr, l], data.get_state(t))


    main()

plot_df(111)
plt.grid(True)
plt.show()