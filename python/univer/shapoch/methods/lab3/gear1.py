from matplotlib import pyplot as plt
from numpy.core import linspace


def gear1_next(a_arr, b_arr, tau):
    a_arr.append(a_arr[-1]/(1 + 0.001 * tau))
    b_arr.append((b_arr[-1]+0.999*a_arr[-1]*tau)/(1+1*tau))


if __name__ == "__main__":
    tau = 0.1
    t_end = 10
    N_tau = int(t_end / tau)

    t_arr = linspace(0, t_end, N_tau + 1)

    y_arr = [2]
    z_arr = [1]

    for t in t_arr:
        gear1_next(z_arr, y_arr, tau)

    plt.plot(y_arr, z_arr)
    plt.show()