from numpy import arange
from math import sin
from matplotlib import pyplot as p

t_arr = arange(0, 10, 0.01)

a = 3
b = 2
A = 12
B = 12
delt = 0

x_arr = [A * sin(a * t + delt) for t in t_arr]
y_arr = [B * sin(b*t) for t in t_arr]

p.plot(x_arr, y_arr)
p.show()

