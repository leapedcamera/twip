import matplotlib
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yaml
import numpy as np
cache_frame_data=False

class Animation():

    def __init__(self, paramFile, t, solution):
        
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.width = data["width"]
        self.height = data["height"]
        self.r = data["r"]
        self.solution = solution
        self.t = t


    def animate(self):
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(autoscale_on=False, xlim=(-2, 2), ylim=(0, 1.75))
        ax.set_aspect('equal')
        ax.grid()

        line, = ax.plot([], [], '-', color='y', lw=2)
        time_template = 'time = %.1fs'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        rect1 = Rectangle((0, 0), self.width, self.height, linewidth=1, edgecolor='k', facecolor='g')
        rect2 = Rectangle((0, 0), -self.width, self.height, linewidth=1, edgecolor='k', facecolor='g')
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ball = plt.Circle((self.r * self.solution[0, 2], self.r), self.r)
        ax.add_patch(ball)

        def animateFrame(i):
            theta = self.solution[i, 2]
            phi = self.solution[i, 0]
            x = self.r * theta
            line.set_data([x, x + self.r * np.sin(theta) ], 
                        [self.r, self.r + self.r * np.cos(theta) ])
            rect1.set(xy=(x, self.r), angle=phi * -180 / np.pi)
            rect2.set(xy=(x, self.r), angle=phi * -180 / np.pi)
            ball.set_center((x, self.r))
            time_text.set_text(time_template % self.t[i])
            return time_text, line, ball, rect1, rect2
        
        ani = animation.FuncAnimation(
            fig, animateFrame, len(self.solution[:, 0]), interval=10, blit=True)
        plt.show()


