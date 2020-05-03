from matplotlib import pyplot as plt
from numpy import arange
import pylab


def get_graph(l, x_start, x_end, step):
    return [l * x * (1 - x) for x in arange(x_start, x_end, step)]


def plot_function(x_0, l, step_count = 100):
    array = [x_0]
    for i in range(step_count): array.append(l * array[-1] * (1 - array[-1]))
    pylab.plot(array, label = f'λ: {l}')
    pylab.legend()


if __name__ == "__main__":
    lambda_arr = [0.5, 1.5, 2.5, 3.75, 3.4]
    x_start = 0
    x_end = 1
    x_step = 0.01
    x_0 = 0.01
    eps = 0.01

    parabola_arr = []
    x_arr = arange(x_start, x_end, x_step)

    plt.figure("with different lambda")
    [plot_function(x_0, each) for each in lambda_arr]

    plt.figure('graphics')
    pylab.plot(x_arr, label = r'$X_{n+1}=X_{n}$')
    [pylab.plot(get_graph(l, x_start, x_end, x_step),label = f'λ: {l}') for l in lambda_arr]
    
    pylab.plot(get_graph(3.4, x_start, x_end, x_step), label = r'$X_{n+1}=λ X_n (1-X_n)$')
    pylab.legend ()

    plt.figure('iteration points')
    plot_function(x_0, 2.9)

    for each in lambda_arr:
        plt.figure(f'graphs with x_0 λ: {each}')
        plot_function(x_0, each)
        plot_function((1 + eps) * x_0, each)
        plt.xlabel(f'$λ: {each}')

    plt.show()
