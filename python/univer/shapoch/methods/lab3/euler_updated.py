from matplotlib import pyplot as plt
from numpy.core import linspace


for tau in [0.1, 0.2, 0.25]:
    y_arr = [2]
    z_arr = [1]

    t_end = 100
    N_tau = int(t_end / tau)
    for t in linspace(0, N_tau * tau, N_tau + 1):
        f_i_j = -y_arr[-1] + 0.999 * z_arr[-1]
        y_arr.append(y_arr[-1] + tau * (-(y_arr[-1] + tau/2*f_i_j) + 0.999 * (z_arr[-1] + tau/2)))
        z_arr.append(z_arr[-1] + tau * (-0.001 * (z_arr[-1] + tau/2*f_i_j)))

    plt.plot(y_arr, z_arr, label=f'tau: {tau}')

plt.legend()
plt.show()