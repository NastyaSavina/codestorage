from math import *
from numpy.core import arange
from matplotlib import pyplot as plt

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


    h = 0.1
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
        plt.plot(u_arr)  
    plt.show()
