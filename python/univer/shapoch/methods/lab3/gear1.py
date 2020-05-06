from matplotlib import pyplot as plt
from numpy.core import linspace, arange


def gear1_next(a_arr, b_arr, tau):
    a_arr.append(a_arr[-1]/(1 + 0.001 * tau))
    b_arr.append((b_arr[-1]+0.999*a_arr[-1]*tau)/(1+1*tau))


if __name__ == "__main__":

    for tau in [0.1, 0.2, 0.25]:
        y = 2
        z = 1
        y_arr = [y]
        z_arr = [z]

        t_arr = arange(0, 100, tau)

        for t in t_arr:
            gear1_next(z_arr, y_arr, tau)

        plt.plot(y_arr, z_arr, label=f'tau: {tau}')
    
    plt.legend()
    plt.show()