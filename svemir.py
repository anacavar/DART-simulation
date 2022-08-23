import numpy as np
import matplotlib.pyplot as plt

class Sustav():
    def __init__(self):
        self.tijela = []
        self.time = [0]

    def __initial_impulse(self):
        # ukupna količina gibanja izoliranog sustava mora biti = 0
        p_x0 = 0
        p_y0 = 0
        for tijelo in self.tijela:
            r0, r0_kut, v0, v0_kut = self.__get_polar_coordinates(tijelo, 0)
            p_x0 += tijelo.mass*v0*np.cos(v0_kut)
            p_y0 += tijelo.mass*v0*np.sin(v0_kut)
        # predajemo negativni izračunati impuls suncu kako bi ukupan impuls sustava bio = 0
        sunce = self.tijela[0]
        v_x0 = -p_x0/sunce.mass
        v_y0 = -p_y0/sunce.mass
        sunce.v[0] = v0
        sunce.v[0] = (np.array((v_x0, v_y0)))

    def __get_polar_coordinates(self, tijelo, i=-1):
        r0 = np.sqrt(tijelo.x[i]**2+tijelo.y[i]**2)
        r0_kut = np.arctan2(tijelo.y[i], tijelo.x[i])
        v0 = np.sqrt(np.dot(tijelo.v[i], tijelo.v[i]))
        v0_kut = np.arctan2(tijelo.v[i][1], tijelo.v[i][0])
        return r0, r0_kut, v0, v0_kut  

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

    def shootComet(self, asteroid, r0, r0_kut, v0, v0_kut):
        self.tijela.append(asteroid)
        self.asteroid = asteroid
        # preračunavanje kutova iz stupnjeva u radijane
        r0_kut = r0_kut*np.pi/180
        v0_kut = v0_kut*np.pi/180
        # računanje početnih koordinata
        x0 = r0*np.cos(r0_kut)
        y0 = r0*np.sin(r0_kut)
        v_x0 = v0*np.cos(v0_kut)
        v_y0 = v0*np.sin(v0_kut)
        # appendanje početnih vektora
        self.asteroid.r.append(np.array((x0, y0)))
        self.asteroid.v.append(np.array((v_x0, v_y0)))
        self.asteroid.x.append(asteroid.r[-1][0])
        self.asteroid.y.append(asteroid.r[-1][1])

    def evolve(self, dt=60*60*24, t = 2*60*60*24*365.25):
        # prije gibanja postavimo odnose gravitacijskih sila na tijela
        self.__apply_gravity()
        # u svakom trenutku pomaknemo svaki planet za jedan korak
        while self.time[-1]<t:
        # for i in range (500):
            for tijelo in self.tijela:
                tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
                tijelo.move(dt)
            self.time.append(self.time[-1]+dt)
            # provjerimo je li došlo do sudara asteroida i planeta
            if (self.__zemlja_pogodjena()):
                print("Zemlja je pogođena!")
                break
      
    def reverseEvolve(self, dt=60*60*24, t= 2*60*60*24*365.25, max_distance=2*1.495978707*10**11):
        # prije gibanja postavimo odnose gravitacijskih sila na tijela
        self.__apply_gravity()  
        # u svakom trenutku pomaknemo svaki planet za jedan korak                                       
        while self.time[-1]<t:
            for tijelo in self.tijela:
                tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
                tijelo.move(-dt)
            self.time.append(self.time[-1]+dt)
            # ako je udaljenost asteroida veća od maksimalne prekini gibanje
            comet_distance = np.sqrt(np.dot(self.asteroid.r[-1], self.asteroid.r[-1]))
            if (comet_distance >= max_distance):
                break

    def getDistance(self, tijelo1, tijelo2):
        udaljenost = np.sqrt((tijelo1.x[-1]-tijelo2.x[-1])**2+(tijelo1.y[-1]-tijelo2.y[-1])**2)
        return udaljenost

    def __zemlja_pogodjena(self):
        # ova metoda provjerava sjeku li se putanje asteroida i Zemlje u zadanom vremenskom intervalu dt
        zemlja = self.tijela[3]

        # točke pravaca
        x1_zemlje = zemlja.x[-2]
        x2_zemlje = zemlja.x[-1]
        y1_zemlje = zemlja.y[-2]
        y2_zemlje = zemlja.y[-1]

        x1_asteroida = self.asteroid.x[-2]
        x2_asteroida = self.asteroid.x[-1]
        y1_asteroida = self.asteroid.y[-2]
        y2_asteroida = self.asteroid.y[-1]

        # pravac 1 (Zemlja)
        a_zemlje = (y2_zemlje-y1_zemlje)/(x2_zemlje-x1_zemlje)
        b_zemlje = -a_zemlje*x1_zemlje + y1_zemlje
        # pravac 2 (asteroida)
        a_asteroida = (y2_asteroida-y1_asteroida)/(x2_asteroida-x1_asteroida)
        b_asteroida = -a_asteroida*x1_asteroida + y1_asteroida

        # računamo koordinate sudara
        x_collision = (b_asteroida-b_zemlje)/(a_zemlje-a_asteroida)
        y_collision = a_zemlje*x_collision + b_zemlje

        uvjet_zemlja = self.uvjet(x_collision, y_collision, x1_zemlje, x2_zemlje, y1_zemlje, y2_zemlje)
        uvjet_asteroid = self.uvjet(x_collision, y_collision, x1_asteroida, x2_asteroida, y1_asteroida, y2_asteroida)

        if (uvjet_zemlja and uvjet_asteroid):
            # crtaj pravce i njihova sjecišta (radi vizualizacije i testiranja)
            # x_zemlje = np.linspace(-10**15, 10**15)
            # y_zemlje = a_zemlje*x_zemlje+b_zemlje
            # x_asteroida = np.linspace(-10**15, 10**15)
            # y_asteroida = a_asteroida*x_asteroida+b_asteroida
            # plt.plot(x_zemlje, y_zemlje, color = "blue")
            # plt.plot(x_asteroida, y_asteroida, color="red")
            # plt.scatter(x1_asteroida, y1_asteroida, color="red")
            # plt.scatter(x1_zemlje, y1_zemlje, color="blue")
            # plt.scatter(x2_asteroida, y2_asteroida, color="red")
            # plt.scatter(x2_zemlje, y2_zemlje, color="blue")
            # plt.scatter(x_collision, y_collision, color="yellow")
            return True
        else: 
            return False

    def uvjet(self, x, y, x1, x2, y1, y2):
        # ova metoda provjerava nalazi li se sjecište (x, y) na dužini između točaka 1 i 2
        delta = 0 # radi testiranja
        if (x1 < x2):
            if (y1 < y2):
                if ((x1 - delta<=x<=x2 + delta) and (y1 -delta<=y<=y2+delta)):
                    return True
            if (y1 > y2):
                if ((x1-delta<=x<=x2+delta) and (y2-delta<=y<=y1+delta)):
                    return True
        if (x1 > x2):
            if (y1 < y2):
                if ((x2 - delta<=x<=x1+ delta) and (y1-delta<=y<=y2+delta)):
                    return True
            if (y1-delta > y2+delta):
                if ((x2<=x<=x1) and (y2<=y<=y1)):
                    return True
        else:
            return False

    def __apply_gravity(self):
        # uspostavljanje međudjelovanja planeta prije početka gibanja
        for tijelo in self.tijela:
            tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
        # predavanje inicijalnog impulsa Suncu
        self.__initial_impulse()

    def __gravitacija_na_tijelo(self, tijelo):
        # računa i vraća ukupnu akceleraciju na pojedini planet u međudjelovanju sa svim ostalim tijelima u sustavu
        tijela = [i for i in self.tijela]
        tijela.remove(tijelo)
        # isključujemo gravitacijsko međudjelovanje zemlje i asteroida
        if(tijelo == self.asteroid):
            zemlja = self.tijela[3]
            tijela.remove(zemlja)
        F_ukupna = np.array((0, 0))
        for tijelo_i in tijela:
            F_ukupna = np.add(F_ukupna, self.__gravitacija(tijelo, tijelo_i))
        a = F_ukupna/tijelo.mass
        return a

    def __gravitacija(self, planet1, planet2):
        # gravitacijska sila usmjerena od prvog planeta prema drugom
        G = 6.67*10**(-11) # newton-metre2-kilogram−2
        r12 = np.subtract(planet2.r[-1], planet1.r[-1])
        r = np.sqrt(np.dot(r12, r12))
        F = G*planet1.mass*planet2.mass/r**3 * r12 # vektor u smjeru planeta 2
        return F

    def resetSystem(self, i=0):
        for tijelo in self.tijela:
            r0 = tijelo.r[i]
            v0 = tijelo.v[i]
            a0 = tijelo.a[i]
            x0 = tijelo.x[i]
            y0 = tijelo.y[i]
            tijelo.r = []
            tijelo.v = []
            tijelo.a = []
            tijelo.x = []
            tijelo.y = []
            tijelo.r.append(r0)
            tijelo.v.append(v0)
            tijelo.a.append(a0)
            tijelo.x.append(x0)
            tijelo.y.append(y0)

    def clear(self):
        self.time = [0]
        self.tijela = []


