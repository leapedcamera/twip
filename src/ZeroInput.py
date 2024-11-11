import Control
import yaml

class ZeroInput(Control.Control):

    def __init__(self, paramFile):
        Control.Control.__init__(self, paramFile)

    def getInput(self, x):
        return 0
    
    def getInput(self, x):
        return 0