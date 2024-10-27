import Control
import yaml
import numpy as np

class PolePlace(Control):
    def __init__(self, paramFile):
        Control.Control.__init__(self, paramFile)
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.K = data["poles"]
    
    def getInput(self, x):
        error = self.xDes - x
        u = np.matmul(-self.K, error)
        return u