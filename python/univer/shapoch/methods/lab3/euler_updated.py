from matplotlib import pyplot as plt
from numpy.core import linspace

tau = 0.1
t_end = 10
N_tau = int(t_end / tau)

t_arr = linspace(0, t_end, N_tau + 1)

y_arr = [2]
z_arr = [1]

for t in t_arr:
    f_i_j = -y_arr[-1] + 0.999 * z_arr[-1]
    y_arr.append(y_arr[-1] + tau * (-(y_arr[-1] + tau/2*f_i_j) + 0.999 * (z_arr[-1] + tau/2)))
    z_arr.append(z_arr[-1] + tau * (-0.001 * (z_arr[-1] + tau/2*f_i_j)))

plt.plot(y_arr, z_arr)
plt.show()