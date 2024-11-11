import Control
import yaml
from scipy import signal
import numpy as np

class PolePlace(Control.Control):
    def __init__(self, paramFile):
        Control.Control.__init__(self, paramFile)
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
            if "K" in data:
                self.K = data["K"]
            if "poles" in data:
                self.poles = np.array(data["poles"])

    
    def getInput(self, x):
        error =  x - self.xDes
        u = np.matmul(-self.K, error)
        return u
    
    def setGain(self, A, B):
        self.K = signal.place_poles(A, B, self.poles).gain_matrix
    
    # Cheat for now with a library
    def setPoles(self, poles):
        self.poles = poles
        
        
