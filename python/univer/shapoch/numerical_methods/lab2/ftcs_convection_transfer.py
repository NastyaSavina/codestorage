

  
from numpy.core import arange, linspace
import math as m
from matplotlib import pyplot as plt
from solver import FTCS_Solver


def plot_ftcs_convection_transfer(graph_index):
    def fi(x, h = 0):
        res = 0

        if x == 1:
            res = 10
        elif x < 1:
            res = 10 * (1 + x)
        else:
            res = 0

        return res 

    def fi_left(x, t):
        return 0


    def fi_right(x, t):
        return 0


    def f(x, t):
        return 0
   
    def main():
        l = 50
        h = 0.2
        u = 1

        t_arr_print = [0.0, 0.1, 0.5, 1.0, 5.0, 10.0]
        t_start = min(t_arr_print)
        t_end = max(t_arr_print) + 0.000001


        c_start = 0.5
        c_end = 0.5
        c_step = 0.5


        x_arr = arange(h, l, h)
        c_arr = [0.1, 0.2, 0.3, 0.4] # arange(c_start, c_end + 0.0001, c_step)
        c_dict = {}

        for c in c_arr:
            tau = c / u * h
            t_arr = arange(t_start, t_end, tau)

            c_dict[str(c)] = FTCS_Solver(t_start, t_end, l, tau, h, fi)
            c_dict[str(c)].initialize(fi)

            for t in t_arr:
                
                c_dict[str(c)].set_u(
                    0, 
                    t + tau, 
                    0
                    )

                print(f"calculate for t: {round(t, 2)}")
                for x in x_arr:
                    c_dict[str(c)].set_u( 
                        x, 
                        t + tau, 
                        c_dict[str(c)].u(x, t) 
                        - c / 2 * (c_dict[str(c)].u(x + h, t) 
                        - c_dict[str(c)].u(x - h, t))
                        )

                c_dict[str(c)].set_u(
                    l, 
                    t + tau, 
                    0
                    )
                    

        for t in t_arr_print:
            plt.figure(str(t))
            for c in c_arr:
                all_x_arr = [0, *x_arr, l]
                c_solver = c_dict[str(c)]
                plt.plot(all_x_arr, c_solver.get_state(t), label = f'c:{c}')
            plt.legend()

    main()
    
plot_ftcs_convection_transfer(111)
plt.show()




    main()
    
plot_ftcs_convection_transfer(111)

plt.show()
