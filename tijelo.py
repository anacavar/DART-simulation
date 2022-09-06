import numpy as np
class Tijelo():
    def __init__(self, masa, radijus, id, color):
        self.mass = masa
        self.rad = radijus
        self.r = []
        self.v = []
        self.a = []
        self.x = []
        self.y = []
        self.id = id
        self.color = color

    def move(self, dt):
        self.v.append(np.add(self.v[-1], self.a[-1]*dt))
        self.r.append(np.add(self.r[-1], self.v[-1]*dt))
        self.x.append(self.r[-1][0])
        self.y.append(self.r[-1][1])

    def clear(self):
        self.r = []
        self.v = []
        self.a = []
        self.x = []
        self.y = []
