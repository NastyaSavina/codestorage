import matplotlib.pyplot as plt
from numpy import linspace
import math as m


def main():
    def find_extremum(array, step_count, max_x):
        max_derivative = 110100101011011
        max_derivative_num = 0
        xStep = max_x / (step_count - 1)

        for i in range(2, len(array) - 1):
            if (abs(array[i + 1] - array[i])) < max_derivative:
                max_derivative_num = i
                max_derivative = abs(array[i + 1] - array[i])

        return xStep * max_derivative_num

    def plot_f9(figure: int):

        plt.figure(figure)
        a0 = 2

        def sech(x: float) -> float:
            return 2 / (m.exp(x) + m.exp(-x))

        def f(x: float) -> float:
            return m.pi / 3 * a0 * (20 * x * m.tanh(m.pow(4 * x, -1))
                                    - 2 * x * m.tanh(m.pow(x, -1))
                                    - 3 * m.pow(sech(m.pow(4 * x, -1)), 2))

        part_count = 10000
        max_x = 2
        input_arr = linspace(0.001, max_x, part_count)
        res = list(map(lambda each: f(each), input_arr))

        max_val = find_extremum(res, part_count, max_x)
        print(f"min_der: {max_val}")
        plt.axvline(x=max_val, color='r', linestyle='-')
        plt.plot(input_arr, res)

    def plot_v(figure: int):
        def v(x: float) -> float:
            l = 1
            k = 1
            return -m.sin(2 * m.pi * x / l) + k * m.sin(4 * m.pi * x / l)

        plt.figure(figure)
        u = -2
        w = 4

        def v_a(x: float) -> float:
            return (u - w) * v(x)

        def v_b(x: float) -> float:
            return (u + w) * v(x)

        input_arr = linspace(0, 10, 1000)

        output_v = list(map(lambda each: v(each), input_arr))
        output_v_a = list(map(lambda each: v_a(each), input_arr))
        output_v_b = list(map(lambda each: v_b(each), input_arr))

        plt.subplot(3, 1, 1)
        plt.plot(input_arr, output_v)

        plt.subplot(3, 1, 2)
        plt.plot(input_arr, output_v_a)

        plt.subplot(3, 1, 3)
        plt.plot(input_arr, output_v_b)

    def plot_u(figure: int, kappa: float, normalize: float):
        def sigma(j: float) -> float:
            return (1 + m.pow((-1), j + 1)) / (m.pi * j)

        def kroneker_symbol(a: int, b: int) -> int:
            return 1 if a == b else 0

        def v_for_teilor(g: int, kappa_f: float) -> float:
            return - kroneker_symbol(1, g) \
                   + kroneker_symbol(-1, g) \
                   - kappa_f * kroneker_symbol(2, g) \
                   + kappa_f * kroneker_symbol(-2, g)

        def u(q, j: float, kappa: float) -> float:
            u = 1
            w = 1
            return (u + w * sigma(j)) * v_for_teilor(q, kappa)

        def k(q: float) -> float:
            L = 1
            return (2 * m.pi / L) * q

        def w(tau, j) -> float:
            return 2 * m.pi * j / tau

        plt.figure(figure)
        output_arr_re = []
        output_arr_im = []
        j_min = -10
        j_max = 10
        part_count = 20
        max_x = 2
        x_arr = linspace(0.01, max_x, part_count)

        for tau in x_arr:
            summ_re = 0
            summ_im = 0

            if tau == 0:
                continue

            for q in range(-2, 3):
                if q == 0:
                    continue
                for j in range(j_min, j_max):
                    if j == 0:
                        continue
                    for q2 in range(-2, 3):
                        if q2 == 0:
                            continue
                        for j2 in range(j_min, j_max):
                            if j2 == 0:
                                continue
                            if q + q2 == 0:
                                continue
                            if j + j2 == 0:
                                continue

                            summ_re += (m.pow(k(q), 2) * m.pow(k(q + q2), 2) * k(q2) * u(q, j, kappa)
                                        * u(q2, j2, kappa) * u(-q - q2, -j - j2, kappa) * m.pow(k(q), 2)
                                        * w(j + j2, tau) - w(j, tau) * m.pow(k(q + q2), 2)) \
                                       / ((m.pow(k(q), 4) + m.pow(w(j, tau), 2))
                                          * (m.pow((q + q2), 4) + m.pow(w((j + j2), tau), 2)))

                            summ_im += (m.pow(k(q), 2) * m.pow(k(q + q2), 2) * k(q2) * u(q, j, kappa)
                                        * u(q2, j2, kappa) * u(-q - q2, -j - j2, kappa)
                                        * ((m.pow(k(q), 2) * m.pow(k(q + q2), 2)) -
                                           (w(tau, j) ** 2) * w(tau, j + j2))) \
                                       / ((k(q) ** 4 + w(tau, j) ** 2) * (k(q + q2) ** 4 + w(tau, j + j2) ** 2))

            output_arr_re.append(summ_re / 2000 + normalize)
            output_arr_im.append(summ_im / 2000 / 2)

        max_val = find_extremum(output_arr_re, part_count, max_x)
        print(f"min_der: {max_val}")
        plt.axvline(x=max_val, color='r', linestyle='-')
        plt.plot(x_arr, output_arr_re)

    plot_f9(figure=1)
    plot_v(figure=2)
    plot_u(figure=3, kappa=1, normalize=2)
    plot_u(figure=4, kappa=-1, normalize=0)

    plt.show()


if __name__ == "__main__":
    main()