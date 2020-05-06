


from numpy.core import arange, linspace
import math as m
from matplotlib import pyplot as plt
from solver import FTCS_Solver

def plot_ftcs_convection_transfer(graph_index):
    def fi(x, h):
        res = 0

        if x == 0 or x == h:
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
        # tau = 0.05
        h = 0.1
        u = 1

        t_arr_print = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 5.0, 10, 20, 30]

        t_start = min(t_arr_print)
        t_end = max(t_arr_print) + 0.00001

        c_start = 0.5
        c_end = 0.5
        c_step = 0.5


        x_arr = arange(2*h, l, h)
        c_arr = arange(c_start, c_end + 0.0001, c_step)


        for c in c_arr:
            tau = c / u * h
            t_arr = arange(t_start, t_end, tau)

            data = FTCS_Solver(t_start, t_end, l, tau, h, fi)
            data.initialize(fi)


            for t in t_arr:
                data.set_u(
                    0, 
                    t + tau, 
                    0
                    )
                
                data.set_u(
                    h,
                    t + tau, 
                    0
                )

                print(f"calculate for t: {round(t, 2)}")
                for x in x_arr:
                    data.set_u( 
                        x, 
                        t + tau, 
                        data.u(x, t) - c * (data.u(x, t) - data.u(x - h, t))
                        )

                data.set_u(
                    l, 
                    t + tau, 
                    0
                    )
                    
                if t in t_arr_print:
                    print(c)
                    print(t)
                    plt.figure(str(round(t, 2)))
                    plt.subplot(graph_index)
                    plt.plot([0, h, *x_arr, l], data.get_state(t))


    main()
    
plot_ftcs_convection_transfer(111)

plt.show()