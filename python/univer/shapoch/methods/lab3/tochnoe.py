import math as m
from numpy.core import arange
from matplotlib import pyplot as plt
import pylab

a_original = [[-1, 0.999], 
              [0, -0.001]]

a_revert   = [[-1,  -999], 
              [0,  -1000]]

a_original_norm = 0
a_revert_norm = 0

for i in range(2):
    s = 0
    s_revert = 0

    for j in range(2):
        s += abs(a_original[i][j])
        s_revert += abs(a_revert[i][j])

    if s > a_original_norm: a_original_norm = s
    if s_revert > a_revert_norm: a_revert_norm = s_revert

obuslow = a_original_norm * a_revert_norm

print(obuslow)

for tau in [0.1, 0.2, 0.25]:
    y = 2
    z = 1
    y_arr = [y]
    z_arr = [z]
    t_arr = arange(0, 100, tau)

    for t in t_arr:
        y_arr.append(m.exp(-t) + m.exp(-0.001*t))
        z_arr.append(m.exp(-0.001 * t))

    plt.plot(y_arr, z_arr, label=f'tau: {tau}')

plt.legend()
plt.show()