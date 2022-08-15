import numpy as np
from tijelo import Tijelo

class Sustav():
    def __init__(self):
        self.tijela = []
        self.time = [0]

    def addPlanet(self, planet, r0, r0_kut, v0, v0_kut):
        self.tijela.append(planet)
        # preračunavanje kutova iz stupnjeva u radijane
        r0_kut = r0_kut*np.pi/180
        v0_kut = v0_kut*np.pi/180
        # računanje početnih koordinata
        x0 = r0*np.cos(r0_kut)
        y0 = r0*np.sin(r0_kut)
        v_x0 = v0*np.cos(v0_kut)
        v_y0 = v0*np.sin(v0_kut)
        # appendanje početnih vektora
        planet.r.append(np.array((x0, y0)))
        planet.v.append(np.array((v_x0, v_y0)))
        planet.x.append(planet.r[-1][0])
        planet.y.append(planet.r[-1][1])

    def shootComet(self, komet, r0, r0_kut, v0, v0_kut):
        self.tijela.append(komet)
        self.komet = komet
        # preračunavanje kutova iz stupnjeva u radijane
        r0_kut = r0_kut*np.pi/180
        v0_kut = v0_kut*np.pi/180
        # računanje početnih koordinata
        x0 = r0*np.cos(r0_kut)
        y0 = r0*np.sin(r0_kut)
        v_x0 = v0*np.cos(v0_kut)
        v_y0 = v0*np.sin(v0_kut)
        # appendanje početnih vektora
        komet.r.append(np.array((x0, y0)))
        komet.v.append(np.array((v_x0, v_y0)))
        komet.x.append(komet.r[-1][0])
        komet.y.append(komet.r[-1][1])

    def evolve(self, dt=2*60*60*24, t = 60*60*24*365.25):
        # prije gibanja postavimo odnose gravitacijskih sila na tijela
        self.__apply_gravity()
        # u svakom trenutku pomaknemo svaki planet za jedan korak
        self.udaljenosti = []
        while self.time[-1]<t:
            for tijelo in self.tijela:
                tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
                tijelo.move(dt)
            self.time.append(self.time[-1]+dt)
            # provjerimo je li došlo do sudara kometa i planeta
            if (self.__planet_pogodjen()):
                print("Planet je pogođen!")
                break
    
    def __get_impact_conditions():
        #code here
        a = 2
        return a

    def __planet_pogodjen(self):
        # gađamo veneru
        planet = self.tijela[2]
        udaljenost_kometa_od_planeta = np.sqrt((planet.x[-1]-self.komet.x[-1])**2+(planet.y[-1]-self.komet.y[-1])**2)/100
        if udaljenost_kometa_od_planeta <= (planet.rad+self.komet.rad):
            return True
        else: 
            return False

    # def __elasticni_sudar(self, tijelo1, tijelo2):
    #     # zakon očuvanja količine gibanja
    #     m1 = tijelo1.mass
    #     r1 = tijelo1.r[-1]
    #     v1 = tijelo1.v[-1]
    #     m2 = tijelo1.mass
    #     r2 = tijelo2.r[-1]
    #     v2 = tijelo2.v[-1]
    #     # ||r2-r1||**2
    #     distance_squared = (tijelo1.x[-1]-tijelo2.x[-1])**2+(tijelo1.y[-1]-tijelo2.y[-1])**2
    #     v1_crtano = v1 - 2*m2/(m1+m2)*np.dot(np.subtract(v1, v2), np.subtract(r1, r2))*np.subtract(r1, r2)/(distance_squared)
    #     v2_crtano = v2 - 2*m1/(m1+m2)*np.dot(np.subtract(v2, v1), np.subtract(r2, r1))*np.subtract(r2, r1)/(distance_squared)
    #     tijelo1.v.pop()
    #     tijelo1.v.append(v1_crtano)
    #     tijelo2.v.pop()
    #     tijelo1.v.append(v2_crtano)

    def __apply_gravity(self):
        # uspostavljanje međudjelovanja planeta prije početka gibanja
        for tijelo in self.tijela:
            tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))

    def __gravitacija_na_tijelo(self, tijelo):
        # računa i vraća ukupnu akcečeraciju na pojedini planet u međudjelovanju sa svim ostalim tijelima u sustavu
        tijela = [i for i in self.tijela]
        tijela.remove(tijelo)
        F_ukupna = np.array((0, 0))
        for tijelo_i in tijela:
            F_ukupna = np.add(F_ukupna, self.__gravitacija(tijelo, tijelo_i))
        a = F_ukupna/tijelo.mass
        return a

    def __gravitacija(self, planet1, planet2):
        #gravitacijska sila usmjerena od prvog planeta prema drugom
        G = 6.67*10**(-11) #newton-metre2-kilogram−2
        r12 = np.subtract(planet2.r[-1], planet1.r[-1])
        r = np.sqrt(np.dot(r12, r12))
        F = G*planet1.mass*planet2.mass/r**3 * r12 # vektor u smjeru planeta 2
        return F

    def clear(self):
        self.time = [0]
        self.tijela = []


   