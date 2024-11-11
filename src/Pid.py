import Control
import yaml

class Pid(Control.Control):
    def __init__(self, paramFile):
        Control.Control.__init__(self, paramFile)
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.Kp = data["Kp"]
        self.Ki = data["Ki"]
        self.Kd = data["Kd"]
        self.prevError = 0
        self.sumError = 0
    
    def getInput(self, x, dt):
        error = self.xDes[0]  - x[0]  
        deltaError = ( error - self.prevError ) / dt
        self.sumError = self.sumError + error * dt
        self.prevError = error
        u = self.Kp * error + self.Ki * self.sumError + self.Kd * deltaError
        return u