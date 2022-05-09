import numpy as np
from planet import Planet

class Sustav():
    def __init__(self, sunce):
        self.Sunce = sunce
        self.Sunce.x.append(0)
        self.Sunce.y.append(0)
        self.Sunce.vx.append(0)
        self.Sunce.vy.append(0)
        self.Sunce.ax.append(0)
        self.Sunce.ay.append(0)
        self.planeti = []
        self.time = [0]
        pass

    def addPlanet(self, planet):
        self.planeti.append(planet)
        print(self.planeti[-1].mass)
        planet.x.append(planet.r0)
        planet.vx.append(0)
        planet.y.append(0)
        planet.vy.append(planet.v0)
        Fgx, Fgy=self.__gravitacija(planet)
        ax=Fgx/planet.mass
        ay=Fgy/planet.mass
        planet.ax.append(ax)
        planet.ay.append(ay)
        
    def __gravitacija(self, planet):
        r = np.sqrt(planet.x[-1]**2+planet.y[-1]**2)
        # G = 6.67*10**(-11) #newton-metre2-kilogram−2.
        G = 1
        Fg = G*planet.mass*self.Sunce.mass/r**2
        theta = np.arctan(abs((planet.y[-1])/(planet.x[-1])))
        #prvi kvadrant
        if planet.x[-1]>=0 and planet.y[-1]>=0:
            Fg_x = -Fg*np.cos(theta)
            Fg_y = -Fg*np.sin(theta)
        #drugi kvadrant
        if planet.x[-1]<0 and planet.y[-1]>=0:
            Fg_x = Fg*np.cos(theta)
            Fg_y = -Fg*np.sin(theta)
        #treći kvadrant
        if planet.x[-1]<0 and planet.y[-1]<0:
            Fg_x = Fg*np.cos(theta)
            Fg_y = Fg*np.sin(theta)
        #četvrti kvadrant
        if planet.x[-1]>=0 and planet.y[-1]<0:
            Fg_x = -Fg*np.cos(theta)
            Fg_y = Fg*np.sin(theta)
        return Fg_x, Fg_y

        
    def evolve(self, dt=0.1, t = 100):
        while self.time[-1]<t:
            self.Sunce.move()
            for planet in self.planeti:
                Fgx, Fgy=self.__gravitacija(planet)
                ax=Fgx/planet.mass
                ay=Fgy/planet.mass
                planet.move(ax, ay, dt)
            self.time.append(self.time[-1]+dt)

    # U REALNIM MJERNIM JEDINICAMA
    def __gravitacija1(self, planet):
        r = np.sqrt(planet.x[-1]**2+planet.y[-1]**2)
        G = 6.67*10**(-11) #newton-metre2-kilogram−2.
        # G = 1
        Fg = G*planet.mass*self.Sunce.mass/r**2
        theta = np.arctan(abs((planet.y[-1])/(planet.x[-1])))
        #prvi kvadrant
        if planet.x[-1]>=0 and planet.y[-1]>=0:
            Fg_x = -Fg*np.cos(theta)
            Fg_y = -Fg*np.sin(theta)
        #drugi kvadrant
        if planet.x[-1]<0 and planet.y[-1]>=0:
            Fg_x = Fg*np.cos(theta)
            Fg_y = -Fg*np.sin(theta)
        #treći kvadrant
        if planet.x[-1]<0 and planet.y[-1]<0:
            Fg_x = Fg*np.cos(theta)
            Fg_y = Fg*np.sin(theta)
        #četvrti kvadrant
        if planet.x[-1]>=0 and planet.y[-1]<0:
            Fg_x = -Fg*np.cos(theta)
            Fg_y = Fg*np.sin(theta)
        return Fg_x, Fg_y


    # broj sekundi u godini 31536000
    # broj sekundi u danu 86400
    def evolve1(self, dt=86400, t = 31536000):
        while self.time[-1]<t:
            self.Sunce.move()
            for planet in self.planeti:
                Fgx, Fgy=self.__gravitacija1(planet)
                ax=Fgx/planet.mass
                ay=Fgy/planet.mass
                planet.move(ax, ay, dt)
            self.time.append(self.time[-1]+dt)


        


        




