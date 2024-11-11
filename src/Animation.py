import matplotlib
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yaml
import numpy as np
cache_frame_data=False

class Animation():

    def __init__(self, paramFile, t, x_hist, u_hist):
        
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
        self.width = data["width"]
        self.height = data["height"]
        self.r = data["r"]
        self.u_hist = u_hist
        self.x_hist = x_hist
        self.t = t
        self.style = data["style"]

    def plotStates(self):

        if self.style == "twip":
            # Plot the results
            plt.plot(self.t, self.x_hist[:, 0], label='phi')
            plt.plot(self.t, self.x_hist[:, 1], label='phi_dot')
            plt.plot(self.t, self.x_hist[:, 2], label='theta')
            plt.plot(self.t, self.x_hist[:, 3], label='theta_dot')
            plt.xlabel('Time')
            plt.ylabel('Values')
            plt.legend()
            plt.show()
        elif self.style == "cart":
           # Plot the results
            plt.plot(self.t, self.x_hist[:, 0], label='x')
            plt.plot(self.t, self.x_hist[:, 1], label='x_dot')
            plt.plot(self.t, self.x_hist[:, 2], label='phi')
            plt.plot(self.t, self.x_hist[:, 3], label='phi_dot')
            plt.xlabel('Time')
            plt.ylabel('Values')
            plt.legend()
            plt.show()
        # Plot the results
        plt.plot(self.t, self.u_hist, label='u')
        plt.xlabel('Time')
        plt.ylabel('Input')
        plt.legend()
        plt.show()

    def animate(self):
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(autoscale_on=False, xlim=(-5, 5), ylim=(0, 1.75))
        ax.set_aspect('equal')
        ax.grid()

        line, = ax.plot([], [], '-', color='y', lw=2)
        time_template = 'time = %.1fs'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        rect1 = Rectangle((0, 0), self.width, self.height, linewidth=1, edgecolor='k', facecolor='g')
        rect2 = Rectangle((0, 0), -self.width, self.height, linewidth=1, edgecolor='k', facecolor='g')
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ball = plt.Circle((self.r * self.x_hist[0, 2], self.r), self.r)
        ax.add_patch(ball)

        def animateTwip(i):
            theta = self.x_hist[i, 2]
            phi = self.x_hist[i, 0]
            x = self.r * theta
            line.set_data([x, x + self.r * np.sin(self.theta) ], 
                        [self.r, self.r + self.r * np.cos(self.theta) ])
            rect1.set(xy=(x, self.r), angle=phi * -180 / np.pi)
            rect2.set(xy=(x, self.r), angle=phi * -180 / np.pi)
            ball.set_center((x, self.r))
            time_text.set_text(time_template % self.t[i])
            return time_text, line, ball, rect1, rect2
        
        def animateCart(i):
            x = self.x_hist[i, 0]
            phi = self.x_hist[i, 2]
            rect1.set(xy=(x, self.r), angle=(phi - np.pi) * 180 / np.pi)
            rect2.set(xy=(x, self.r), angle=(phi - np.pi) * 180 / np.pi)
            ball.set_center((x, self.r))
            time_text.set_text(time_template % self.t[i])
            return time_text, line, ball, rect1, rect2
        
        if self.style == "cart":
            ani = animation.FuncAnimation(
                fig, animateCart, len(self.x_hist[:, 0]), interval=1, blit=True)
        elif self.style == "twip":
            ani = animation.FuncAnimation(
                fig, animateTwip, len(self.x_hist[:, 0]), interval=1, blit=True)  
        plt.show()


