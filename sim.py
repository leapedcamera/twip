import numpy as np
from numpy import sin, cos
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import ZeroInput
import Dynamics
import Animation

# Set initial conditions
initial_conditions = [0, 0, 0, 0.5]

# Define time points
t = np.linspace(0, 30, 1000)

# Input file
fname = "settings.yml"

# Define control
control = ZeroInput.ZeroInput(fname)

# Define dynamics
dynamics = Dynamics.Dynamics(fname)

# Solve the equations
solution = odeint(dynamics.integrate, initial_conditions, t, args=(control,))

# Produce animation
animation = Animation.Animation(fname, t, solution)
animation.animate()

# Plot the results
plt.plot(t, solution[:, 0], label='phi')
plt.plot(t, solution[:, 1], label='phi_dot')
plt.plot(t, solution[:, 2], label='theta')
plt.plot(t, solution[:, 3], label='theta_dot')
plt.xlabel('Time')
plt.ylabel('Values')
plt.legend()
plt.show()