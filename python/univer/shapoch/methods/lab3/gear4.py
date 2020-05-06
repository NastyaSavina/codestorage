from matplotlib import pyplot as plt
from numpy.core import arange
from gear1 import gear1_next
from gear2 import gear2_next
from gear3 import gear3_next


def gear4_next(a_arr, b_arr, tau):
    a_arr.append((48*a_arr[-1]-36*a_arr[-2]+16*a_arr[-3]-3*a_arr[-4])/(25+12*0.001*tau))
    b_arr.append((48*b_arr[-1]-36*b_arr[-2]+16*b_arr[-3]-3*b_arr[-4]+12*tau*0.999*a_arr[-1])/(25+12*tau))



if __name__ == "__main__":

    for tau in [0.1, 0.2, 0.25]:
        y = 2
        z = 1
        y_arr = [y]
        z_arr = [z]

        gear1_next(z_arr, y_arr, tau)
        gear2_next(z_arr, y_arr, tau)
        gear3_next(z_arr, y_arr, tau)

        t_arr = arange(0, 100, tau)

        for t in t_arr:
            gear4_next(z_arr, y_arr, tau)

        plt.plot(y_arr, z_arr, label=f"tau: {tau}")

    plt.legend()    
    plt.show()