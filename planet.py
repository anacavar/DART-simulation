import numpy as np

class Planet():

    def __init__(self, masa_planeta, r0, v0, r0_kut = 0, v0_kut = 90):
        self.mass = masa_planeta
        self.r0 = r0
        self.v0 = v0
        self.x = []
        self.y = []
        self.vx = []
        self.vy = []
        self.ax = []
        self.ay = []

    def move(self, ax=0, ay=0, dt = 0.01):
        self.ax.append(ax)
        self.ay.append(ay)
        self.x.append(self.x[-1]+ self.vx[-1]*dt)
        self.y.append(self.y[-1]+ self.vy[-1]*dt)
        self.vx.append(self.vx[-1]+ self.ax[-1]*dt)
        self.vy.append(self.vy[-1]+ self.ay[-1]*dt)



    
        