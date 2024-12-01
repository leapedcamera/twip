import numpy as np
import yaml

import Dynamics

from numpy import sin, cos

class RollerDynamics(Dynamics.Dynamics):

    def __init__(self, paramFile):
        
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        l = data["l"]
        mb = data["mb"]
        mw = data["mw"]
        Iw = data["Iw"]
        Ib = data["Ib"]

        self.r = data["r"]
        self.c1 = (mb * self.r * l) / (-Iw - np.power(self.r, 2) * (mb + mw))
        self.c2 = (-mb * l) / (Ib + mb * np.power(l, 2))

    def integrate(self, x, t, u):
               
        g = 9.81
        Sx = sin(x[0])
        Cx = cos(x[0])
        
        phi_dot = x[1]
        phi_double_dot = (-self.c1 * self.c2 * self.r * np.power(x[1], 2) * Sx * Cx - self.c2 * g * Sx) / \
                        (1 - self.c1 * self.c2 * self.r * np.power(Cx, 2))
        theta_dot = x[3] 
        theta_double_dot = (-self.c1 * self.c2 * g * Sx * Cx - self.c1 * np.power(x[1], 2) * Sx) / \
                        (1 - self.c1 * self.c2 * self.r * np.power(Cx, 2)) 
        
        return [phi_dot, phi_double_dot, theta_dot, theta_double_dot]
    
    def integrateLinear( self, x, t, u):
        
        g = 9.81
        phi_dot = x[1]
        phi_double_dot =  -(self.c2 * g * x[0]) / \
                        (1 - self.c1 * self.c2 * self.r)
        theta_dot = x[3] 
        theta_double_dot =  -(self.c1 * self.c2 * g * x[0]) / \
                        (1 - self.c1 * self.c2 * self.r)
        
        return [phi_dot, phi_double_dot, theta_dot, theta_double_dot]