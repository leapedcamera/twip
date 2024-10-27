import Control
import yaml

class Pid(Control):
    def __init__(self, paramFile):
        Control.Control.__init__(self, paramFile)
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.Kp = data["Kp"]
        self.Ki = data["Ki"]
        self.Kd = data["Kd"]
        self.prevError = 0
        self.sumError = 0
    
    def getInput(self, x):
        error = self.xDes[0] - x[0]
        deltaError = error - prevError
        sumError = sumError + error
        prevError = error
        u = self.Kp * error + self.Ki * self.sumErr + self.Kd * deltaError
        return u