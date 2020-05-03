from scipy.stats import norm as normStats
import numpy as np
import math
import random
import matplotlib.pyplot as plt

pointCount = 100
lineCount = 100
momentCount = 1

def f(val):
    tau = 6
    return val + math.sqrt(2*tau) * random.normalvariate(0, 1)

def p(f, t, minVal): 
    res = []
    D = 1

    for i in range(100):
        t[i] = abs(t[i])
        b = math.exp(-((f[i])**2)/(4*D*(t[i]+1)))
        a = b/(2*math.sqrt(math.pi*D*(t[i]+1)))
        res.append(a)

    return res

moment = [[[]]]
xArr = range(pointCount)
yRes = []
xRes = []

for i in range(momentCount-1):
    moment.append([[]])


for i in range(lineCount-1):
    for j in range(momentCount):
        moment[j].append([])


for j in range(lineCount):
    x = 0
    for i in range(pointCount):
        for k in range(momentCount):
            moment[k][j].append(x**(k+1))
        x = f(x)




for k in range(momentCount):
    plt.figure(k+1)

    for i in range(pointCount):
        ySum = 0;
        xSum = 0;
        
        for j in range(lineCount):
            ySum += moment[k][j][i]

        ySum /= lineCount
        plt.subplot(2, 1, 1)
        yRes.append(ySum)

    for j in range(lineCount):
        plt.plot(moment[k][j], color='b')
    
    plt.plot(xArr, yRes, color='r')
    yRes = []

    momentRavel = np.ravel(moment[k])
    minVal = np.min(momentRavel)
    maxVal = np.max(momentRavel)

    arr = [0] * 100
    momentRavelMapped = list(map(lambda a: a - minVal, momentRavel))
    step = (maxVal - minVal) / 99
    points = np.linspace(minVal, maxVal, 100)

    for each in momentRavelMapped:
        val = int(each // step)
        arr[val] = arr[val] + 1


    plt.subplot(2, 1, 2)

    t = list(map(lambda a: (a - minVal) * step , range(100)))
    pArr = p(arr, t, minVal)

    plt.plot(list(map(lambda a: (a * step + minVal), range(100))),pArr, color='r')
    arrBar = list(map(lambda a: a / sum(arr), arr))
    plt.bar(list(map(lambda a: a * step + minVal, range(100))), arrBar)
    
    print(arr)

plt.show()
