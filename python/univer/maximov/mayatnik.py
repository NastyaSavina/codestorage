from matplotlib import pyplot as plt
import numpy
import pylab
import math as m

first = []
two = []

def f(x,y):
    gamma = 0.1
    g = 9.8
    F = 0
    z = 0
    res=-gamma*y-g*m.sin(x)+F*m.cos(z)
    return res

def RungeKutta_4(x_, y, h):
    k1 = f(x_,y)
    k2 = f(x_ + h / 2, y + k1 * h / 2)
    k3 = f(x_ + h / 2, y + k2 * h / 2)
    k4 = f(x_ + h, y + h * k3)
    y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y
x = 0    
y = 0
h = 0.5

for i in range(100):
     y = RungeKutta_4(x, y, h)
     first.append(y)
     two.append(i)

plt.figure('first')
plt.plot(first,two)
plt.show()