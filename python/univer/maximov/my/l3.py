from matplotlib import pyplot as plt
from numpy import arange
import math as m

def touch(s):
    if s['x'][1] <= m.sin(s['x'][0]):
        der = s['speed'][1]/s['speed'][0]
        der_ang = der*180/m.pi if der*180/m.pi < 0 else der*180/m.pi + 360
        der_s = (m.sin(s['x'][0] + 0.00001) - m.sin(s['x'][0]))/(0.00001)
        der_s_v = der_s*180/m.pi
        der_s_v = der_s_v + 360 if der_s < 0 else der_s_v
        ang_s = der_ang - der_s_v + 360 if der_ang - der_s_v > 0 else der_ang - der_s_v
        new_grad = (180 - (der_ang - der_s_v) + der_s_v) % 360
        s['speed'][0] = -(s['speed'][0] ** 2 + s['speed'][1] ** 2) ** 0.5 * m.cos(new_grad)
        s['speed'][1] = -(s['speed'][0] ** 2 + s['speed'][1] ** 2) ** 0.5 * m.sin(new_grad)
        


def get_v(v, g, dt):
    return [v[0], v[1] + g*dt]


def next(s, g, dt):
    touch(s)
    for i in range(2): s['x'][i] = s['x'][i] + s['speed'][i] * dt
    s['speed'] = get_v(s['speed'], g, dt)

g = -9.8
t = {'t0': 0, 't': 30, 'dt': 0.0002}
a = {'x': [0, 3], 'speed': [2.5, 1]}

xs = []
ys = []
dx = 0.01

current_t = t['t0']

while current_t < t['t']:
    next(a, g, t['dt'])
    xs.append(a['x'][0])
    ys.append(a['x'][1])
    current_t = current_t + t['dt']

sin_arr = [m.sin(x) for x in arange(min(xs), max(xs), dx)]

fig, ax = plt.subplots()
ax.plot(xs, ys)
ax.plot(arange(min(xs), max(xs), dx), sin_arr)
plt.show()
