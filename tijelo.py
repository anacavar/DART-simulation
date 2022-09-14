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
        self.travelledDistance = 0

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

    def getTravelledDistance(self):
        self.travelledDistance = 0
        for i in range (0, len(self.r)-1):
            self.travelledDistance+=self.__getDistance(self.r[i],self.r[i+1])
        return self.travelledDistance

    def __getDistance(self, r1, r2):
        udaljenost = np.sqrt((r2[0]-r1[0])**2+(r2[1]-r1[1])**2)
        return udaljenost

