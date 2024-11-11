import numpy as np
import yaml
from yaml import load, dump

class Dynamics:
                
    def getSystem(self):
        A, B = np.nan
        return [A, B]

    def integrateLinear(self, x, t, u):
        [A, B] = self.getSystem()

        dx = np.zeros(4)
        dx = np.matmul(A,x) + B * u
        return dx
    
    def stabilityCheck(self):
        [A, B] = self.getSystem()     
        eigs = np.linalg.eig(A)
        if (eigs.eigenvalues >= 0).any():
            print("System is unstable")
        else:
            print("System is stable")

