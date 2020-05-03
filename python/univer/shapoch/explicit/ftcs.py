import matplotlib.pyplot as plt
import matplotlib.animation as ani
import math

def phi(x):
	return 1 - math.sin(math.pi * x)

def m1(time):
	return 1

def m2(time):
	return 1

def f(x, t):
	return -math.sin(t)

a = 0.5
L = 1
T = 1

dx = 1e-1
dt = 0.5 * dx * dx / a

xNodes = int(L / dx)
tNodes = int(T / dt)

data = []

initial = []
for i in range(xNodes):
	initial.append(phi(i * dx))

data.append(initial)

for t in range(1, tNodes):
	newLayer = []	

	for i in range(xNodes):
		if i == 0:
			newLayer.append(m1(t * dt))
		elif i == xNodes - 1:
			newLayer.append(m2(t * dt))
		else:
			newLayer.append(data[t-1][i] + dt * a / dx / dx *(data[t-1][i+1] - 2 * data[t-1][i] + data[t-1][i-1]) + dt * f(i * dx, t * dt))

	data.append(newLayer)

def animate(n):
    line = plt.plot(data[n], color='g')
    return line

fig = plt.figure()
_a_ = ani.FuncAnimation(fig, animate, frames=len(data), interval=100, blit=True, repeat=False)
plt.show()




