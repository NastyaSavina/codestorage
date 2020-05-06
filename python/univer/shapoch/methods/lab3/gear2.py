from matplotlib import pyplot as plt
from numpy.core import linspace, arange
from gear1 import gear1_next


def gear2_next(a_arr, b_arr, tau):
    a_arr.append((4*a_arr[-1]-a_arr[-2])/(3+0.002*tau))
    b_arr.append((4*b_arr[-1]-b_arr[-2]+2*tau*0.999*a_arr[-1])/(3+2*tau))


if __name__ == "__main__":

    for tau in [0.1, 0.2, 0.25]:
        y = 2
        z = 1
        y_arr = [y]
        z_arr = [z]

        gear1_next(z_arr, y_arr, tau)

        t_arr = arange(0, 100, tau)

        for t in t_arr:
            gear2_next(z_arr, y_arr, tau)

        plt.plot(y_arr, z_arr, label=f'tau: {tau}')
    
    plt.legend()
    plt.show()