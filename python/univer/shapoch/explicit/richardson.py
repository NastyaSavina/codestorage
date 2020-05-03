import matplotlib.pyplot as plt
import matplotlib.animation as ani
from numpy.core import arange
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
data.append(initial)

for t in range(2, tNodes):
	newLayer = []	

	for i in range(xNodes):
		if i == 0:
			newLayer.append(m1(t * dt))
		elif i == xNodes - 1:
			newLayer.append(m2(t * dt))
		else:
			newLayer.append(data[t-2][i] + 2 *a*dt/dx/dx*(data[t-1][i+1] - 2 * data[t-1][i] + data[t-1][i-1]) + 2 * dt * f(i * dx, t * dt))

	data.append(newLayer)

fig = plt.figure()
ax = plt.axes(xlim=(0, 1), ylim=(-100, 100))
line, = ax.plot([])

def animate(n, data):
	global line
	global ax
	print(data[n])
	x_range = range(0, len(data[n]))
	ax.set_xlim(min(x_range), max(x_range))
	ax.set_ylim(min(data[n]), max(data[n]))
	line.set_xdata(x_range)
	line.set_ydata(data[n])
	return line, ax,


_a_ = ani.FuncAnimation(fig, 
		animate, 
		frames=len(data), 
		fargs=([data]),
		interval=500, blit=True, repeat=False)

plt.show()




