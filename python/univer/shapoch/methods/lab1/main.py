from matplotlib import pyplot as plt
from numpy.core import arange
from math import exp, sin, cos, pi

def init_f(x):
    return -1.0

def fi(x):
    return -1.0


def fi_left(x, t):
    return 0


def fi_right(x, t):
    return 0


def f(x, t):
    return x ** 3 - 6 * x * t


def plot_u_from_book(graph_index):
    def a_k(k, t):
        res = -2*exp(pi ** 2 * k ** 2 * t) 
        res *= (pi * k * (6 * t - 1) * sin(pi * k) + (6 * t - 3) * cos(pi * k) - 6 * t)
        res += pi * k * sin(pi * k) + 3 * cos(pi * k)
        res /= (pi ** 4 * k **4)
        return res

    def a_0(t):
        res = 1 / 2
        res *= (t - 6 * t ** 2)
        res += 2
        return res 


    sum_a_k = 0


    h = 0.01
    l = 1
    tau = 0.1
    t_arr = [0, 0.1, 0.5, 1.0, 5.0, 10.0]

    for t in t_arr:

        u_arr = []

        for x in arange(0, l + h, h):
            sum_a_k = 0

            for k in range(1, 3):
                sum_a_k += a_k(k, t) * cos(pi * k * x) * exp(-(pi*k/l)**2 * t)

            u = 0.5 * a_0(t) + sum_a_k

            u_arr.append(u)

        plt.figure(str(round(t, 1)))
        plt.subplot(graph_index)
        plt.grid(True)
        plt.plot(u_arr)  


def plot_ftcs(graph_index):
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
        tau = 0.01
        h = 0.1

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
                    plt.figure(str(round(t, 1)))
                    plt.subplot(graph_index)
                    plt.grid(True)
                    plt.plot([0, *x_arr, l], data.get_state(t))


    main()
    

def plot_df(graph_index):


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
                    plt.grid(True)
                    plt.plot([0, *x_arr, l], data.get_state(t))


    main()


plot_ftcs(311)
plot_df(312)
plot_u_from_book(313)

plt.show()