import numpy as np
from numpy import sin, cos
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import ZeroInput
import PolePlace
import Pid

import RollerDynamics
import CartDynamicsSimple
import CartDynamicsDamping

import Animation

# Set initial conditions
initial_conditions = [0.00, 0, np.pi + .01, 0]

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
x_hist = np.zeros([n,4])
x = initial_conditions
u_hist = np.zeros(n)

# Run the simulation
for i, t_final in enumerate(t):
    # History comes first, but values are from previous step
    u_hist[i] = u
    x_hist[i,:] = x
    t_steps = np.linspace(t_prev, t_final, 2)
    x = odeint(dynamics.integrate, x_hist[i,:], t_steps, args=(u_hist[i],))[1,:]
    u = control.getInput(x, t_final - t_prev)
    t_prev = t_final
    
# Produce animation
animation = Animation.Animation(fname, t, x_hist, u_hist)
animation.animate()
animation.plotStates()