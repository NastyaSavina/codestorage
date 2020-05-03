import numpy as np
import matplotlib.pyplot as plt
import math as m


def v_a(x, v0, l, kappa):
    return v0 * (m.sin(2 * m.pi * x / l) + kappa * m.sin(4 * m.pi * x / l))


def f_exp(sign, beta, x, v0, l, kappa):
    return m.exp(sign * beta * v_a(x, v0, l, kappa))


def integrate(f, left, right):
    step_count = 10
    h = (right - left) / step_count
    return sum(list(map(lambda x: f(x) * h, np.linspace(left, right, step_count + 1))))


def rho(sign, beta, x, l, v0, kappa):
    return f_exp(sign, beta, x, v0, l, kappa) \
           / integrate(lambda var: f_exp(sign, beta, var, v0, l, kappa), 0, l)


def f_on_off(beta, l, v0, kappa):
    return integrate(lambda var: var * rho(-1, beta, var, l, v0, kappa), 0, l) / l - 1 / 2


def f_off_on(beta, l, v0, kappa):
    step_count = 1000
    right = 0
    left = l
    step = (left - right) / step_count
    res_sum = 0

    for i in range(0, step_count):
        res_sum += rho(1, beta, i*step, l, v0, kappa) \
                   * integrate(lambda var: var * rho(-1, beta, var, l, v0, kappa) - 1 / l, 0, i*step)

    return res_sum * step


def a(beta, l, tau, v0, kappa):
    on_off = f_on_off(beta, l, v0, kappa)
    off_on = f_off_on(beta, l, v0, kappa)
    print(f"on_off: {round(on_off, 2)}, off_on: {round(off_on, 2)}, beta: {round(beta, 2)}, l: {round(l, 2)}")
    return (l / tau) * (on_off + off_on)


l_val = 1
tau_val = 0.001
v0_val = 1
kappa_val = 1/4

for beta_val in np.arange(2.3, 640, 2):
    plt.scatter(beta_val, a(beta_val, l_val, tau_val, v0_val, kappa_val), edgecolors='red', c='red')
    plt.pause(0.05)

plt.show()
