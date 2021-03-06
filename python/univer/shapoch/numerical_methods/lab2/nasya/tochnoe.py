from numpy import arange
from matplotlib import pyplot as p

def fi(x, h = 0):
    res = 0

    if x == 1:
        res = 10
    elif x < 1:
        res = 10 * (1 + x)
    else:
        res = 0

    return res 

c_arr = [0.1, 0.5, 0.6, 1.0, 2.5]
h = 0.01
tau = 0.01


x_arr = arange(0, 50, h)

t_arr_print = [0.0, 0.1, 0.5, 1.0, 5.0, 10.0]
t_arr = arange(0, 10 + tau, tau)


for c in c_arr:
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
