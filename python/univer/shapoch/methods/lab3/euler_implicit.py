from matplotlib import pyplot as plt
from numpy.core import linspace


for tau in [0.1, 0.2, 0.25]:
    y_arr = [2]
    z_arr = [1]

    t_end = 100
    N_tau = int(t_end / tau)
    for t in linspace(0, N_tau * tau, N_tau + 1):
        y_arr.append(1/2*(y_arr[-1] + 0.999 * z_arr[-1] * tau / (1 + 0.001 * tau)))
        z_arr.append(z_arr[-1] / (1 + 0.001 * tau))

    plt.plot(y_arr, z_arr, label=f'tau: {tau}')

plt.legend()
plt.show()