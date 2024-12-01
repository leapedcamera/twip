import numpy as np
import Dynamics
import yaml

from numpy import sin, cos

class CartDynamicsDamping(Dynamics.Dynamics):

    def __init__(self, paramFile):
        Dynamics.Dynamics.__init__(self)
        
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.l = data["l"]
        self.mb = data["mb"]
        self.mw = data["mw"]
        self.d = data["d"]
        

    def integrate(self, x, t, u):
        
        g = -10
        Sx = np.sin(x[2])
        Cx = np.cos(x[2])
        D = self.mb * self.l * self.l * (self.mw + self.mb * (1 - np.power(Cx,2)))
        dx = np.zeros(4)
        dx[0] = x[1]
        dx[1] = (1/D) * (-np.power(self.mb, 2) * np.power(self.l, 2) * g * Cx * Sx + self.mb * \
                       np.power(self.l, 2) * (self.mb * self.l * np.power(x[3],2) * Sx - self.d * x[1])) + \
                        self.mb * self.l * self.l * (1/D) * u
        dx[2] = x[3]
        dx[3] = (1/D) * ((self.mb+self.mw) * self.mb * g * self.l * Sx - self.mb * self.l * Cx \
                         * (self.mb * self.l * np.power(x[3],2) * Sx - self.d * x[1])) - \
                            self.mb * self.l * Cx * (1/D) * u
        
        return dx
    
    def getSystem(self):
        
        g = -10
        A = np.zeros([4,4])
        A[0,1] = 1
        A[1,1] = -self.d / self.mw
        A[1,2] = self.mb * g / self.mw
        A[2,3] = 1
        A[3,1] = -self.d / self.mw / self.l
        A[3,2] = -(self.mw + self.mb) * g / self.mw / self.l

        B = np.zeros(4)
        B[1] = 1 / self.mw
        B[3] = 1 / self.l / self.mw
        return [A, np.array(np.matrix(B).T)]