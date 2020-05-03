from math import *
from numpy.core import arange
from matplotlib.pyplot import plot, show

def x_fi(ro, fi):
    return ro*cos(fi)

def y_fi(ro, fi):
    return -ro*sin(fi)


fi_arr = arange(-0, 12, 0.01)
ro = 1

x_arr = [x_fi(ro, fi) for fi in fi_arr]
y_arr = [y_fi(ro, fi) for fi in fi_arr]

plot(x_arr, y_arr)
show()
