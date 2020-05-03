from matplotlib import pyplot as plt
from numpy.core import arange
from math import pow


def f(x, a, lambd1, lambd2):
    print(lambd2 / lambd1)
    return a * (x ** (lambd2 / lambd1))


if __name__ == "__main__":
    x_arr = arange(0, 1, 0.0001)
    a_arr = arange(-20, 20, 3)

    l1 = (-1 + (17 ** 0.5)) / 4
    l2 = (-1 - (17 ** 0.5)) / 4

    for a in a_arr:
        y_arr = [f(x, a, l1, l2) for x in x_arr]
        plt.plot(x_arr, y_arr)

    plt.show()