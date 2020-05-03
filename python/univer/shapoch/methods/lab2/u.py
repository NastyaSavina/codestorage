import math as m
from numpy.core import arange
from matplotlib import pyplot as plt

def fi_0(x):
    return 1

def fi_n(x, n, l):
    return 2 / (m.pi * n) * m.sin(2 * m.pi * x / l)

def f_0(t, l):
    return 1 / 4 - 3 * t

def f_n(t, n, l):
    return ((m.pi ** 3 + n ** 3 * (1 - 6*t) - 6 * m.pi * n)*m.sin(m.pi * n)+6*m.pi**2*n**2*t+ (3 * m.pi**2*n**2*(1-2*t)-6)*m.cos(m.pi * n + 6))/ (n ** 4 * m.pi ** 4)


from math import sin


def work(f, a, b, n):
    print("\nТекущее число разбиений: ", n)
    h = (b-a)/float(n)
    print("Текущий шаг:", h)
    total = sum([f((a + (k*h))) for k in range(0, n)])
    result = h * total
    print("Текущий результат: ", result)
    return result


def f(x):
    return sin(x)/x

if __name__ == "__main__":
    l = 1.0
    h = 0.01
    t = 0
    a = 1
    n = 1

    x_arr = arange(0, l + h, h)
    t_arr = [0.0, 0.1, 0.5, 1.0, 5.0, 10.0]#arange(0, 0.2, 0.1)

    for t in t_arr: 
        u_arr = []
        
        for x in x_arr:
            sum_fi = 0
            sum_f_n = 0

            for n in range(1, 2):
                sum_fi += 2*fi_n(x, n, l) * m.exp(-((n*n)*(m.pi*m.pi)*t)/(l**2))
            
            sum_f_n += 2*(m.exp((m.pi**2)*(n**2))*(t**3)/6)*f_n(t, n, l)*m.cos(m.pi*n*x/l)

            u_next = fi_0(x)\
                        + 1/4*(t-6*(t**2))\
                        + sum_fi\
                        + sum_f_n

            print(f"t: {t}")
            print(f"x: {x}")
            print(f"sum_fi: {sum_fi}")
            print(f"sum_f_n: {sum_f_n}")

            u_arr.append(u_next/1e7-7)

        plt.figure(str(round(t, 1)))
        plt.plot(x_arr, u_arr)

    plt.show()