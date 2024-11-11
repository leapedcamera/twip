import numpy as np
import yaml
from yaml import load, dump

class Control:
    def __init__(self, paramFile):
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.xDes = data["xDes"]
        self.uHistory = np.empty

    def saveInput(self, u):
        self.uHistory = np.append(self.uHistory, u)
    
    def getInput(self):
        return self.uHistory