import matplotlib.pyplot as plt

def recalculate_v(v, g, dt):
    v_x = v[0]
    v_y = v[1]
    v_x_new = v_x
    v_y_new = v_y + g*dt
    return [v_x_new, v_y_new]


def accounding_walls(stone):
    if stone['r'][1] <= 0:
        stone['v'][1] = -stone['v'][1]

    if stone['r'][0] >= 100:
        stone['v'][0] = - stone['v'][0]


def next_position(stone, g, dt):
    accounding_walls(stone)

    stone['r'][0] = stone['r'][0] + stone['v'][0] * dt
    stone['r'][1] = stone['r'][1] + stone['v'][1] * dt

    stone['v'] = recalculate_v(stone['v'], g, dt)

g = -9.8
t = {'start': 0, 'end': 4, 'step': 0.001}

x = 0
y = 3
vx = 50
vy = 0

stone = {'r': [x, y], 'v': [vx, vy]}

x_arr = []
y_arr = []

current_t = t['start']

while current_t < t['end']:
    next_position(stone, g, t['step'])
    x_arr.append(stone['r'][0])
    y_arr.append(stone['r'][1])
    current_t = current_t + t['step']

plt.plot(x_arr, y_arr)
plt.show()