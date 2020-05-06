import math as m
from numpy.core import arange
from matplotlib import pyplot as plt
import pylab

for tau in [0.1, 0.2, 0.25]:
    y = 2
    z = 1
    y_eiler_arr = [y]
    z_eiler_arr = [z]

    t_arr = arange(0, 100, tau)

    for t in t_arr:
        print(f"t: {t}")
        y = y + tau * (-y + 0.999 * z)
        z = z + tau * (-0.001 * z)
        y_eiler_arr.append(y)
        z_eiler_arr.append(z)

    plt.plot(y_eiler_arr, z_eiler_arr, label=f'tau: {round(tau, 2)}')

plt.legend()
plt.show()