import numpy as np
from numpy import sin, cos
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import ZeroInput
import PolePlace
import Pid
import Lqr

import RollerDynamics
import CartDynamicsSimple
import CartDynamicsDamping

import Animation


# Set initial conditions
initial_conditions = [0.00, 0, np.pi + .1, 0]

# Define time points
dt = .001
sim_length = 10
t = np.linspace(dt, sim_length, int(sim_length / dt) )
n = np.size(t)
t_prev = 0

# Input file
fname = "config/settings.yml"

# Define dynamics
dynamics = CartDynamicsDamping.CartDynamicsDamping(fname)
dynamics.stabilityCheck()

# Define control
control = Pid.Pid(fname)
[A,B] = dynamics.getSystem()
#control.setGain(A,B)
u = 0

# Data holders
xHist = np.zeros([n,4])
x = initial_conditions
uHist = np.zeros(n)

# Run the simulation
for i, t_final in enumerate(t):
    # History comes first, but values are from previous step
    uHist[i] = u
    xHist[i,:] = x
    t_steps = np.linspace(t_prev, t_final, 2)
    x = odeint(dynamics.integrate, xHist[i,:], t_steps, args=(uHist[i],))[1,:]
    u = control.getInput(x, t_final - t_prev)
    t_prev = t_final
    
# Produce animation
animation = Animation.Animation(fname, t, xHist, uHist)

animation.plotStates()
animation.plotError()
animation.animate()