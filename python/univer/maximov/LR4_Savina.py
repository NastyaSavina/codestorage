import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pylab

sigma=10
r=28
b=8/3
def f(y, t):
    y1, y2, y3 = y
    return [sigma*(y2-y1),-y2+(r-y3)*y1,-b*y3+y1*y2]


t = np.linspace(0,20,2001)
y0 = [1, -1, 10]
[y1,y2,y3]=odeint(f, y0, t, full_output=False).T
fig = plt.figure('first') 
ax=Axes3D(fig)
ax.plot(y1,y2,y3,linewidth=2)
plt.xlabel('y1')
plt.ylabel('y2')
plt.title("Initial conditions:  [1, -1, 10]")

fig = plt.figure('velosity1') 
plt.plot(t,y1)
plt.title("x Components (1, -1, 10)")


y0 = [1.0001, -1, 10]
[y1_1,y2,y3]=odeint(f, y0, t, full_output=False).T
fig = plt.figure('second') 
ax=Axes3D(fig)
ax.plot(y1_1,y2,y3,linewidth=2)
plt.xlabel('y1')
plt.ylabel('y2')
plt.title("Initial conditions:  [1.0001, -1, 10]")

fig = plt.figure('velosity2') 
plt.plot(t,y1_1)
plt.title("x Components (1.0001, -1, 10)")

plt.figure('x_Components')
pylab.plot (y1, 'r--', label = 'x Components (1, -1, 10)')
pylab.plot (y1_1, 'b-', label = 'x Components (1.0001, -1, 10)')
pylab.legend ()

plt.figure('Сomponent difference')
pylab.plot (t,abs(y1_1-y1))


plt.show()