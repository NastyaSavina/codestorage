from numpy import arange
from matplotlib import pyplot as p

def fi(x):
    res = 0

    if x == 0:
        res = 10
    elif x <= 1:
        res = 10 * (1 - x)

    return res 

c = 1.0
h = 0.01
tau = 0.01


x_arr = arange(0, 50, h)

t_arr_print = [0.0, 0.1, 0.5, 1.0, 5.0, 10.0]
t_arr = arange(0, 10 + tau, tau)

for t in t_arr:
    y_t = []
    for x in x_arr:
        if t <= x / c:
            y_t.append(fi(x - c * t))
        else:
            y_t.append(0)

    if round(t, 5) in t_arr_print:
        p.figure(str(round(t, 1)))
        p.plot(x_arr, y_t)

p.show()
