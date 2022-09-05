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
        
    def launch(self, letjelica, putanjaAsteroida, putanjaZemlje, N_do_trenutka_pogotka=1):
        # koordinate ispaljivanja letjelice (prva točka evolucije === zadnja (-1) točka reverse evolucije Zemlje)
        x1 = putanjaZemlje[-1][0] + 1000000
        y1 = putanjaZemlje[-1][1] + 1000000
        # koordinate sudare letjelice i meteora (n-ta točka evolucije === -n-ta točka reverse evolucije asteroida)
        x2 = putanjaAsteroida[-N_do_trenutka_pogotka][0]
        y2 = putanjaAsteroida[-N_do_trenutka_pogotka][1]
        # postavljanje početne pozicije letjelice
        letjelica.r.append(np.array((x1, y1)))
        letjelica.x.append(x1)
        letjelica.y.append(y1)
        self.tijela.append(letjelica)
        # postavljanje početne brzine letjelice
        t = N_do_trenutka_pogotka*self.dt
        s = np.sqrt((x2-x1)**2+(y2-y1)**2)
        v0 = s/t
        v0_kut = np.arctan2(y2-y1, x2-x1)
        v_x0 = v0*np.cos(v0_kut)
        v_y0 = v0*np.sin(v0_kut)
        letjelica.v.append(np.array((v_x0, v_y0)))

    def reverseEvolve(self, dt=60*60*24, t= 2*60*60*24*365.25, max_distance=2*1.495978707*10**11):
        self.dt = dt
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

    def evolve(self, dt=60*60*24, t = 2*60*60*24*365.25):
        # prije gibanja postavimo odnose gravitacijskih sila na tijela
        self.__apply_gravity()
        # u svakom trenutku pomaknemo svaki planet za jedan korak
        while self.time[-1]<t:
            for tijelo in self.tijela:
                tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
                tijelo.move(dt)
            self.time.append(self.time[-1]+dt)
            # provjerimo je li došlo do sudara asteroida i planeta
            if (self.__zemlja_pogodjena()):
                print("Zemlja je pogođena!")
                break
            # # provjerimo je li došlo do sudara letjelice s asteroidom
            if (self.__asteroid_pogodjen()):
                print("Asteroid je pogođen")

    def __zemlja_pogodjena(self):
        for tijelo in self.tijela:
            if (tijelo.id == "Zemlja"):
                zemlja = tijelo
        return self.__sudar_tijela(zemlja, self.asteroid)

    def __asteroid_pogodjen(self):
        for tijelo in self.tijela:
            if (tijelo.id == "letjelica"):
                letjelica = tijelo
        return self.__sudar_tijela(self.asteroid, letjelica)

    def __sudar_tijela(self, tijelo1, tijelo2):
        # ova metoda provjerava sjeku li se putanje dvaju tijela u zadanom vremenskom intervalu dt
        # točke pravaca
        x1_tijela1 = tijelo1.x[-2]
        x2_tijela1 = tijelo1.x[-1]
        y1_tijela1 = tijelo1.y[-2]
        y2_tijela1 = tijelo1.y[-1]
        x1_tijela2 = tijelo2.x[-2]
        x2_tijela2 = tijelo2.x[-1]
        y1_tijela2 = tijelo2.y[-2]
        y2_tijela2 = tijelo2.y[-1]
        # pravac 1 (tijelo1)
        a_tijela1 = (y2_tijela1-y1_tijela1)/(x2_tijela1-x1_tijela1)
        b_tijela1 = -a_tijela1*x1_tijela1 + y1_tijela1
        # pravac 2 (tijelo2)
        a_tijela2 = (y2_tijela2-y1_tijela2)/(x2_tijela2-x1_tijela2)
        b_tijela2 = -a_tijela2*x1_tijela2 + y1_tijela2
        # računamo koordinate sudara
        x_collision = (b_tijela2-b_tijela1)/(a_tijela1-a_tijela2)
        y_collision = a_tijela1*x_collision + b_tijela1
        # provjeravamo uvjete da se dužine sjeku
        uvjet_tijelo1 = self.__uvjet(x_collision, y_collision, x1_tijela1, x2_tijela1, y1_tijela1, y2_tijela1)
        uvjet_tijelo2 = self.__uvjet(x_collision, y_collision, x1_tijela2, x2_tijela2, y1_tijela2, y2_tijela2)
        if (uvjet_tijelo1 and uvjet_tijelo2):
            # crtaj pravce i njihova sjecišta (radi vizualizacije i testiranja)
            # x_tijela1 = np.linspace(-10**15, 10**15)
            # y_tijela1 = a_tijela1*x_tijela1+b_tijela2
            # x_tijela2 = np.linspace(-10**15, 10**15)
            # y_tijela2 = a_tijela2*x_tijela2+b_tijela2
            # plt.plot(x_tijela1, y_tijela1, color = "blue")
            # plt.plot(x_tijela2, y_tijela2, color="red")
            # plt.scatter(x1_tijela2, y1_tijela2, color="red")
            # plt.scatter(x1_tijela1, y1_tijela1, color="blue")
            # plt.scatter(x2_tijela2, y2_tijela2, color="red")
            # plt.scatter(x2_tijela1, y2_tijela1, color="blue")
            # plt.scatter(x_collision, y_collision, color="yellow")
            return True
        else:
            return False

    def __uvjet(self, x, y, x1, x2, y1, y2):
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
        # iz liste tijela koje gravitacijski djeluju na zadani planet mičemo zadani planet i letjelicu
        tijela.remove(tijelo)
        for body in tijela:
            if (body.id == 'letjelica'):
                tijela.remove(body)
        # isključujemo gravitacijsko međudjelovanje zemlje i asteroida
        if(tijelo == self.asteroid):
            zemlja = self.tijela[3]
            tijela.remove(zemlja)
        # isključujemo gravitacijsko djelovanje za letjelicu
        if (tijelo.id == "letjelica"):
            return 0*tijelo.v[-1]
        # računamo ukupnu akceleraciju na pojedini planet
        F_ukupna = np.array((0, 0))
        for tijelo_i in tijela:
            F_ukupna = np.add(F_ukupna, self.__gravitacija(tijelo, tijelo_i)) #Tuu (neš se unutra dogodi kad krene evolucija pozitivna)
        a = F_ukupna/tijelo.mass
        return a

    def __gravitacija(self, planet1, planet2):
        # gravitacijska sila usmjerena od prvog planeta prema drugom
        G = 6.67*10**(-11) # newton-metre2-kilogram−2
        r12 = np.subtract(planet2.r[-1], planet1.r[-1])
        # print(r12)
        r = np.sqrt(np.dot(r12, r12))
        F = G*planet1.mass*planet2.mass/r**3 * r12 # vektor u smjeru planeta 2
        return F


    def resetSystem(self, i=0):
        self.time = [0]
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