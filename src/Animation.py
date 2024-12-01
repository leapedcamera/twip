import matplotlib
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yaml
import numpy as np
cache_frame_data=False

class Animation():

    def __init__(self, paramFile, t, xHist, uHist):
        
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.width = data["width"]
        self.height = data["height"]
        self.r = data["r"]
        self.uHist = uHist
        self.xHist = xHist
        self.t = t
        self.style = data["style"]
        self.xDes = data["xDes"]

    def plotError(self):
        error = self.xHist - self.xDes
        if self.style == "twip":
            # Plot the results
            plt.plot(self.t, error[:, 0], label='phi')
            plt.plot(self.t, error[:, 1], label='phi_dot')
            plt.plot(self.t, error[:, 2], label='theta')
            plt.plot(self.t, error[:, 3], label='theta_dot')
            plt.xlabel('Time')
            plt.ylabel('Error')
            plt.title("Twip Error States")
            plt.legend()
            plt.show()
        elif self.style == "cart":
           # Plot the results
            plt.plot(self.t, error[:, 0], label='x')
            plt.plot(self.t, error[:, 1], label='x_dot')
            plt.plot(self.t, error[:, 2], label='phi')
            plt.plot(self.t, error[:, 3], label='phi_dot')
            plt.xlabel('Time')
            plt.ylabel('Error')
            plt.title("Cart Error States")
            plt.legend()
            plt.show()
        plt.show()

    def plotStates(self):

        if self.style == "twip":
            # Plot the results
            plt.plot(self.t, self.xHist[:, 0], label='phi')
            plt.plot(self.t, self.xHist[:, 1], label='phi_dot')
            plt.plot(self.t, self.xHist[:, 2], label='theta')
            plt.plot(self.t, self.xHist[:, 3], label='theta_dot')
            plt.xlabel('Time')
            plt.ylabel('Values')
            plt.title("TWIP States")
            plt.legend()
            plt.show()
        elif self.style == "cart":
           # Plot the results
            plt.plot(self.t, self.xHist[:, 0], label='x')
            plt.plot(self.t, self.xHist[:, 1], label='x_dot')
            plt.plot(self.t, self.xHist[:, 2], label='phi')
            plt.plot(self.t, self.xHist[:, 3], label='phi_dot')
            plt.xlabel('Time')
            plt.ylabel('Values')
            plt.title("Cart States")
            plt.legend()
            plt.show()
        # Plot the results
        plt.plot(self.t, self.uHist, label='u')
        plt.xlabel('Time')
        plt.ylabel('Input')
        plt.title("Control Signal")
        plt.legend()
        plt.show()

    def animate(self):
        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(autoscale_on=False, xlim=(-5, 5), ylim=(0, 1.75))
        ax.set_aspect('equal')
        ax.grid()

        line, = ax.plot([], [], '-', color='y', lw=2)
        time_template = 'TIME = %.1fs'
        time_text = ax.text(.01, .8, '', fontsize=20, transform=ax.transAxes, weight='bold')
        rect1 = Rectangle((0, 0), self.width, self.height, linewidth=1, edgecolor='k', facecolor='g')
        rect2 = Rectangle((0, 0), -self.width, self.height, linewidth=1, edgecolor='k', facecolor='g')
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ball = plt.Circle((self.r * self.xHist[0, 2], self.r), self.r)
        ax.add_patch(ball)

        def animateTwip(i):
            theta = self.xHist[i, 2]
            phi = self.xHist[i, 0]
            x = self.r * theta
            line.set_data([x, x + self.r * np.sin(self.theta) ], 
                        [self.r, self.r + self.r * np.cos(self.theta) ])
            rect1.set(xy=(x, self.r), angle=phi * -180 / np.pi)
            rect2.set(xy=(x, self.r), angle=phi * -180 / np.pi)
            ball.set_center((x, self.r))
            time_text.set_text(time_template % self.t[i])
            return time_text, line, ball, rect1, rect2
        
        def animateCart(i):
            x = self.xHist[i, 0]
            phi = self.xHist[i, 2]
            rect1.set(xy=(x, self.r), angle=(phi - np.pi) * 180 / np.pi)
            rect2.set(xy=(x, self.r), angle=(phi - np.pi) * 180 / np.pi)
            ball.set_center((x, self.r))
            time_text.set_text(time_template % self.t[i])
            return time_text, ball, rect1, rect2
        
        if self.style == "cart":
            ani = animation.FuncAnimation(
                fig, animateCart, len(self.xHist[:, 0]), interval=1, blit=True)
        elif self.style == "twip":
            ani = animation.FuncAnimation(
                fig, animateTwip, len(self.xHist[:, 0]), interval=1, blit=True)  
        plt.show()


