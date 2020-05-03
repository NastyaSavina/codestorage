import numpy as np
import matplotlib.pyplot as plt
import math as m
import scipy.integrate as integrate

eps = 1.e-3
lim = 40
rep = 40


def my_integrate(func, left, right):
    stepCount = 100
    valArr = np.linspace(left, right, stepCount + 1)

    valArrFunc = list(map(lambda each: ))


def v_a(x, v0, l, k):
    return v0 * (m.sin(2 * m.pi * x / l) + k * (m.sin(4 * m.pi * x / l)))


def rho_exp(coef, beta, x, v0, l, k):
    return m.exp(coef * beta * v_a(x=x, v0=v0, l=l, k=k))


def rho(x, beta, coef, v0, l, k):
    top = rho_exp(coef, beta, x, v0, l, k)
    bot = integrate.quad(lambda each: rho_exp(coef=coef, beta=beta, x=each, v0=v0, l=l, k=k), 0, l, epsabs=eps, epsrel=eps, limit=lim, limlst=rep)[0]
    return top / bot


def phi_off_on_internal(beta, v0, l, k, x):
    return integrate.quad(lambda each: rho(x=each, beta=beta, coef=-1, v0=v0, l=l, k=k) - 1 / l, 0, x, epsabs=eps, epsrel=eps, limit=lim, limlst=rep)[0]


def phi_off_on(x, beta, v0, l, k):
    return integrate.quad(lambda each: rho(x=each, beta=beta, coef=1, v0=v0, l=l, k=k)
                                       * phi_off_on_internal(beta=beta, v0=v0, l=l, k=k, x=x),
                          0,
                          l, epsabs=eps, epsrel=eps, limit=lim, limlst=rep)[0]


def avg_x(beta, v0, l, k):
    return integrate.quad(lambda each: each * rho(x=each, beta=beta, coef=-1, v0=v0, l=l, k=k), 0, l, epsabs=eps, epsrel=eps, limit=lim, limlst=rep)[0]


def phi_on_off(beta, v0, l, k):
    return avg_x(beta=beta, v0=v0, l=l, k=k) / l - 1 / 2


def u(x, beta, v0, l, k, tau):
    print(beta)
    print("\n")
    return (l / tau) * (phi_off_on(x=x, beta=beta, v0=v0, l=l, k=k) + phi_on_off(beta, v0, l, k))


x_start = 4
v0_start = 1
l_start = 1
k_start = 1/4
tau_start = 1

beta_arr = np.linspace(40, 500, (500 - 40) / 20)

beta_arr_res = list(map(lambda each: u(x=x_start, beta=each, v0=v0_start, l=l_start, k=k_start, tau=tau_start), beta_arr))
beta_arr_ln = list(map(lambda each: m.log(each, m.e), beta_arr))
plt.figure(1)
plt.plot(beta_arr_ln, beta_arr_res)
plt.figure(2)
plt.plot(beta_arr, beta_arr_res)
plt.show()
