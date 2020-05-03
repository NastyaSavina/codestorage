# -*- coding: utf-8 -*-
"""
This function create a phase portrait of ode

Created on Mon Jan 23 18:51:01 2017
Copyright 2017 Sinitsa AM site: digiratory.ru

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.


@author: Sinitsa AM digiratory.ru
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

'''
In this function you should implement your ode
for example:
d*theta/dt = omega
d*omega/dt = -b*omega - c*np.sin(theta)

@args:
    y - state variable
    t - time
    b, c - args of ode
'''
def ode(y, t, b, c):
        theta, omega = y
        dydt = [omega, -b*omega - c*np.sin(theta)]
        return dydt
        

'''
Calculate ode

@args:
    args - arguments of ODE
    y0 - The initial state of y
    yd0 - The initial state of derivative y
    ts - the duration of the simulation
    nt - Number steps if simulation (=ts*deltat)
'''
def calcODE(args, y0, dy0, ts = 10, nt = 101):
    y0 = [y0, dy0]
    t = np.linspace(0, ts, nt)
    sol = odeint(ode, y0, t, args)
    return sol

'''
Drawing Phase portrait of ODE in function ode()

@args:
    args - arguments of ODE
    deltaX - step  x
    deltaDX - step  derivative x
    startX - start value of x
    stopX - stop value of x
    startDX - start value of derivative x
    stopDX - stop value of derivative x
    ts - the duration of the simulation
    nt - Number steps if simulation (=ts*deltat)
'''    
def drawPhasePortrait(args, deltaX = 1, deltaDX = 1, startX = 0,  stopX = 5, startDX = 0, stopDX = 5, ts = 10, nt = 101):
    for y0 in range(startX, stopX, deltaX):
            for dy0 in range(startDX, stopDX, deltaDX):
                sol = calcODE(args, y0, dy0, ts, nt)
                plt.plot(sol[:, 0], sol[:, 1], 'b')
    plt.xlabel('x')
    plt.ylabel('dx/dt')
    plt.grid()
    plt.show()
    
      
b = 0.25
c = 5.0
args=(b, c)
drawPhasePortrait(args)
drawPhasePortrait(args, 1, 1, -10, 10, -5, 5, ts = 30, nt = 301)