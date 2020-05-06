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

dx = 1e-2
dt = 1e-1

xNodes = int(L / dx)
tNodes = int(T / dt)

initial = list(map(lambda each: phi(each * dx), range(xNodes)))

data = initial

for t in range(1, tNodes):
	newLayer = [0] * xNodes

	alpha = [0] * xNodes
	betta = [0] * xNodes

	alpha[1] = 0
	betta[1] = m1(t * dt)

	r = a * dt / 2 / (dx ** 2)

	A = -r
	B = -r
	C = 1 + 2 * r

	for i in range(2, xNodes):
		alpha[i] = -B / (A * alpha[i-1] + C)
		betta[i] = (data[t-1][i - 1] + r * (data[t-1][i] 
						- 2 * data[t-1][i - 1] 
						+ data[t-1][i-2]) 
						+ dt * f((i - 1) * dx, t * dt) 
						- A * betta[i - 1]) \
					/ (A * alpha[i - 1] +  C)

	newLayer[xNodes - 1] = m2(t * dt)

	for i in range(xNodes - 2, -1, -1):
		newLayer[i] = alpha[i + 1] * newLayer[i + 1] + betta[i + 1]

	data.append(newLayer)

def animate(n):
    line = plt.plot(data[n], color='g')
    return line

fig = plt.figure()
_a_ = ani.FuncAnimation(fig, animate, frames=len(data), interval=100, blit=True, repeat=False)
plt.show()
