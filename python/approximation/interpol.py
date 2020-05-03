from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

x = [1,2,3,4]
y = [4,5,6,7]

f = interpolate.interp1d(x, y, kind='cubic')

x_arr = np.linspace(1,4,11)

plt.plot(x_arr, f(x_arr))

plt.show()
