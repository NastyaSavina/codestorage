from numpy.core import arange, linspace
import math as m
from matplotlib import pyplot as plt
from solver import FTCS_Solver

def plot_ftcs_convection_transfer(graph_index):
    def fi(x):
        res = 0

        if x == 0:
            res = 10
        elif x <= 1:
            res = 10 * (1 - x)

        return res 

    def fi_left(x, t):
        return 0


    def fi_right(x, t):
        return 0


    def f(x, t):
        return 0
   
    def main():
        l = 50
        tau = 0.05
        h = 0.1

        t_arr_print = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 5.0, 10.0, 20, 30, 40, 50, 60, 70]

        t_start = min(t_arr_print)
        t_end = max(t_arr_print) + tau

        d_start = 0.1
        d_end = 0.1
        d_step = 0.1


        x_arr = arange(h, l, h)
        t_arr = arange(t_start, t_end, tau)
        d_arr = arange(d_start, d_end + 0.0001, d_step)


        for d in d_arr:
            data = FTCS_Solver(t_start, t_end, l, tau, h, fi)
            data.initialize(fi)

            for t in t_arr:
                data.set_u(
                    0, 
                    t + tau, 
                    0
                    )

                print(f"calculate for t: {round(t, 2)}")
                for x in x_arr:
                    data.set_u( 
                        x, 
                        t + tau, 
                        data.u(x, t) \
                        - d / 2 * (data.u(x + h, t) - data.u(x - h, t)) + \
                        (d**2)/2*(data.u(x + h, t) - 2*data.u(x, t)+data.u(x - h, t))
                        )

                data.set_u(
                    l, 
                    t + tau, 
                    0
                    )
                    
                if t in t_arr_print:
                    print(d)
                    print(t)
                    plt.figure(str(round(t, 2)))
                    plt.subplot(graph_index)
                    plt.plot([0, *x_arr, l], data.get_state(t))


    main()
    
plot_ftcs_convection_transfer(111)

plt.show()