import numpy as np
import yaml

from numpy import sin, cos

class Dynamics():

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

    def integrate(self, x, t, control):
        
        u = control.getInput(x)
        Sx = sin(x[0])
        Cx = cos(x[0])
        
        phi_dot = x[1]
        phi_double_dot = (-self.c1 * self.c2 * self.r * np.power(x[1], 2) * Sx * Cx - self.c2 * 9.81 * Sx) / \
                        (1 - self.c1 * self.c2 * self.r * np.power(Cx, 2))
        theta_dot = x[3]
        theta_double_dot = (-self.c1 * self.c2 * 9.81 * Sx * Cx - self.c1 * np.power(x[1], 2) * Sx) / \
                        (1 - self.c1 * self.c2 * self.r * np.power(Cx, 2)) + u
        
        control.saveInput(u)
        
        return [phi_dot, phi_double_dot, theta_dot, theta_double_dot]