from matplotlib import pyplot as plt
from numpy.core import linspace
from gear1 import gear1_next
from gear2 import gear2_next
from gear3 import gear3_next


def gear4_next(a_arr, b_arr, tau):
    a_arr.append((48*a_arr[-1]-36*a_arr[-2]+16*a_arr[-3]-3*a_arr[-4])/(25+12*0.001*tau))
    b_arr.append((48*b_arr[-1]-36*b_arr[-2]+16*b_arr[-3]-3*b_arr[-4]+12*tau*0.999*a_arr[-1])/(25+12*tau))



if __name__ == "__main__":
    tau = 0.1
    t_end = 10
    N_tau = int(t_end / tau)

    t_arr = linspace(0, t_end, N_tau + 1)

    y_arr = [2]
    z_arr = [1]

    gear1_next(z_arr, y_arr, tau)
    gear2_next(z_arr, y_arr, tau)
    gear3_next(z_arr, y_arr, tau)

    for t in t_arr:
        gear4_next(z_arr, y_arr, tau)

    plt.plot(y_arr, z_arr)
    plt.show()