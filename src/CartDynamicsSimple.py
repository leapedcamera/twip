import numpy as np
import Dynamics
import yaml

from numpy import sin, cos

class CartDynamicsSimple(Dynamics.Dynamics):

    def __init__(self, paramFile):
        
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.l = data["l"]
        self.mb = data["mb"]
        self.mw = data["mw"]

    def integrate(self, x, t, u):
        
        g = -9.81
        Sx = np.sin(x[2])
        Cx = np.cos(x[2])
        D = self.mw + self.mb * np.power(Sx,2)
        
        dx = np.zeros(4)
        dx[0] = x[1]
        dx[1] = (1/D) * (u + self.mb * Sx * ( g * Cx + self.l * np.power(x[3], 2)))
        dx[2] = x[3]
        dx[3] = (1/D/self.l) * (-u * Cx - self.mb * self.l * np.power(x[3], 2) * Sx * Cx - (self.mb + self.mw) * g * Sx)
        
        return dx
    
    def getSystem(self):
        
        g = -9.81        
        A = np.zeros([4,4])
        A[0,1] = 1
        A[1,2] = self.mb * g / self.mw
        A[2,3] = 1
        A[3,2] = (self.mb + self.mb) * g / self.l / self.mw

        B = np.zeros(4)
        B[1] = 1 / self.mw
        B[3] = 1 / self.l / self.mw
        return [A, np.matrix(B).T]
    