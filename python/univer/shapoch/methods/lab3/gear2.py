from matplotlib import pyplot as plt
from numpy.core import linspace
from gear1 import gear1_next


def gear2_next(a_arr, b_arr, tau):
    a_arr.append((4*a_arr[-1]-a_arr[-2])/(3+0.002*tau))
    b_arr.append((4*b_arr[-1]-b_arr[-2]+2*tau*0.999*a_arr[-1])/(3+2*tau))


if __name__ == "__main__":
    tau = 0.1
    t_end = 10
    N_tau = int(t_end / tau)

    t_arr = linspace(0, t_end, N_tau + 1)

    y_arr = [2]
    z_arr = [1]

    gear1_next(z_arr, y_arr, tau)

    for t in t_arr:
        gear2_next(z_arr, y_arr, tau)

    plt.plot(y_arr, z_arr)
    plt.show()