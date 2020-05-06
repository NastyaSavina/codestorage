import math as m
from numpy.core import arange
import matplotlib.pyplot as plt


def multiplier(k, n):
    return m.factorial(n) / (m.factorial(k) * m.factorial(n - k))


def b(k, n, t):
    return multiplier(k, n) * (t ** k) * ((1 - t) ** (n - k))


def beze_interpolate(x_arr, y_arr):
    B_x = []
    B_y = []

    for t in arange(0, 1.01, 0.001):
        res_x = 0
        res_y = 0

        for i in range(len(x_arr)):
            res_x = res_x + x_arr[i]*b(i, len(x_arr) - 1, t)
            res_y = res_y + y_arr[i]*b(i, len(y_arr) - 1, t)
        
        B_x.append(res_x)
        B_y.append(res_y)
    return {'x': B_x, 'y': B_y}

def main():
    lag = 4
    next_days = 24
    w_k = 0.01

    y = [1, 1, 1, 1, 1, 
         6, 6, 6, 6, 6, 
         6, 9, 9, 12, 27, 
         27, 36, 36, 51, 51, 
         69, 76, 76, 81, 81, 
         86, 86, 94, 94, 94, 
         152, 152, 163, 304, 
         351, 440, 562, 700, 
         861, 1100]
    
    x = range(0, len(y))
    B_x = []
    B_y = []

    k_calc_arr = (list(map(lambda l, r: r - l, y[:-1], y[1:])))[-2:]
    k = k_calc_arr[1] / k_calc_arr[0]
    print(k)

    y_future = y[:]

    for i in range(0, next_days):
        y_future.append(y_future[len(y_future) - 1] + (y_future[len(y_future) - 1] - y_future[len(y_future) - 2]) * k)
    x_future = range(0, len(y_future))
    B_x_future = []
    B_y_future = []

    y_future_without_k = y[:]
    for i in range(0, next_days):
        y_future_without_k.append(y_future_without_k[len(y_future_without_k) - 1] + (y_future_without_k[len(y_future_without_k) - 1] - y_future_without_k[len(y_future_without_k) - 2]) * 1)
    x_future_without_k = range(0, len(y_future_without_k))
    B_x_future_without_k = []
    B_y_future_without_k = []

    B = beze_interpolate(x, y)
    B_future = beze_interpolate(x_future, y_future)
    B_future_without_k = beze_interpolate(x_future_without_k, y_future_without_k)

    B_future_without_k['x'] = [round(each, 1) for each in B_future_without_k['x']]
    B_future_with_lag = {}
    B_future_with_lag['x'] = [each - lag for each in B_future['x'] if each - lag >= 0]
    B_future_with_lag['y'] = B_future['y'][-len(B_future_with_lag['x']):]

    print(B_future_without_k['x'])

    today_x = max(B['x'])
    nearest_x = 0
    diff = 1000

    for each in B_future_without_k['x']:
        if abs(each - today_x) < diff:
            diff = abs(each - today_x)
            nearest_x = each
    

    print(nearest_x)
    i = B_future_without_k['x'].index(nearest_x)
    
    
    plt.axvline(B_future_without_k['x'][i], color='black')
    
    plt.hlines(B_future_without_k['y'][i], 0, B_future_without_k['x'][i], color='black')
    plt.hlines(B_future_with_lag['y'][i], 0, B_future_with_lag['x'][i], color='black')
    
    plt.plot(B_future['x'], B_future['y']) 
    plt.plot(B_future_with_lag['x'], B_future_with_lag['y']) 
    plt.plot(B_future_without_k['x'], B_future_without_k['y'])
    plt.plot(B['x'], B['y'])

    plt.gca().set_xlim(min(B_future['x']) - max(B_future['x']) * w_k, max(B_future['x']) * (1 + w_k))
    plt.gca().set_ylim(min(B_future['y']) - max(B_future['y']) * w_k, max(B_future['y']) * (1 + w_k))
    plt.minorticks_on()
    plt.grid(b=True, which='major')
    plt.grid(b=True, which='minor')
    plt.show()


if __name__ == "__main__":
    main()