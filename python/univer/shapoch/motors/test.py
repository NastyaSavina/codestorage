import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math

# 1000 simulations of die roll
n = 10000

avg = []
for i in range(1,n):#roll dice 10 times for n times
    a = np.random.randint(1,7,10)#roll dice 10 times from 1 to 6 & capturing each event
    avg.append(np.average(a))#find average of those 10 times each time

plt.hist(avg[0:],20,density=100)

zscore = stats.zscore(avg[0:])

mu, sigma = np.mean(avg), np.std(avg)
s = np.random.normal(mu, sigma, 10000)

# Create the bins and histogram
count, bins, ignored = plt.hist(s, 20, density=100)

# Plot the distribution curve
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (bins - mu)**2 / (2 * sigma**2)))