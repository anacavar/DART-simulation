import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

class Sustav():
    def __init__(self):
        self.tijela = []
        self.time = [0]
        self.x_pogotka_letjelice = None
        self.y_pogotka_letjelice = None
        self.N_do_lansiranja = 0
        self.letjelica_stop = False
        self.ZemljaPogodjenaBoolean = False
        self.min_udaljenost = []

    def reverseEvolve(self, dt=60*60, t= 2*60*60*24*365.25, max_distance=2*1.495978707*10**11, metoda="RK"):
        self.dt = dt
        # u svakom trenutku pomaknemo svaki planet za jedan korak
        while self.time[-1]<t:
            for tijelo in self.tijela:
                tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
                if(metoda=="RK"):
                    self.__move_RungeKutta(tijelo, -dt) # Runge Kutta metoda
                elif(metoda=="euler"):
                    tijelo.move(dt) # Eulerova metoda
            self.time.append(self.time[-1]+dt)
            # ako je udaljenost asteroida veća od maksimalne prekini gibanje
            # asteroid_distance = np.sqrt(np.dot(self.asteroid.r[-1], self.asteroid.r[-1])) #absolute distance from the Sun
            asteroid_distance = self.asteroid.getTravelledDistance() # travelled distance
            if (asteroid_distance >= max_distance):
                # print(f"prijeđena udaljenost je: {self.asteroid.getTravelledDistance()/(1.496*10**11)}")
                self.N_koraka = len(self.time)-1
                break

    def evolve(self, dt=60*60, t = 2*60*60*24*365.25, metoda="RK"):
        self.ZemljaPogodjenaBoolean = False
        # u svakom trenutku pomaknemo svaki planet za jedan korak
        for i in range(self.N_koraka):
            for tijelo in self.tijela:
                if(tijelo.id == "letjelica"):
                    if(len(self.time)-1>=self.N_do_lansiranja and self.letjelica_stop == False): # letjelica lansirana
                        tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
                        tijelo.move(dt)
                else:
                    tijelo.a.append(self.__gravitacija_na_tijelo(tijelo))
                    if(metoda=="RK"):
                        self.__move_RungeKutta(tijelo, dt) # Runge Kutta metoda
                    elif(metoda=="euler"):
                        tijelo.move(dt) # Eulerova metoda
            self.time.append(self.time[-1]+dt)
            # provjerimo je li došlo do sudara asteroida i planeta
            # self.__zemlja_pogodjena()
            if (self.getDistance2(self.Zemlja.r[-1], self.asteroid.r[-1])<self.Zemlja.rad+self.asteroid.rad):
                print("Zemlja je pogođena!") 
                self.ZemljaPogodjenaBoolean = True
                break
            # provjerimo je li došlo do sudara letjelice s asteroidom (ali samo ako postoji letjelica i ako je lansirana)
            if(self.tijela[-1].id == "letjelica"):
                if(len(self.time)-1>=self.N_do_lansiranja): # provjera samo ako je letjelica lansirana 
                    if(len(self.tijela[-1].r)>=2):
                        if (self.__asteroid_pogodjen()): # je li letjelica pogodila asteroid
                            if (self.letjelica_stop == False): # ako letjelica nije već udarila komet
                                print("Asteroid je pogođen")
                                self.__inelastic_collision(self.letjelica, self.asteroid) # perfect inelastic collision applied

    def __inelastic_collision(self, tijelo1, tijelo2):
        m1 = tijelo1.mass
        m2 = tijelo2.mass
        v1 = tijelo1.v[-1]
        v2 = tijelo2.v[-1]
        v_ukupno = np.add(m1*v1, m2*v2)/(m1+m2)
        # print(self.asteroid.v[-1])
        self.asteroid.v.pop()
        self.asteroid.v.append(v_ukupno)
        # print(self.asteroid.v[-1])
        self.letjelica_stop = True
        self.N_konačni_letjelice = self.time[-1]/self.dt
        return v_ukupno

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

    def addPlanet(self, planet, r0, r0_kut, v0, v0_kut):
        if (planet.id == "Zemlja"):
            self.Zemlja = planet
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
        
    def launch(self, letjelica, putanjaAsteroida, putanjaZemlje, N_do_lansiranja=0,  N_do_pogotka=0):
        self.letjelica_stop = False
        self.N_do_lansiranja = N_do_lansiranja
        # koordinate ispaljivanja letjelice
        x1 = putanjaZemlje[N_do_lansiranja][0] +1000000
        y1 = putanjaZemlje[N_do_lansiranja][1] +1000000
        # koordinate sudare letjelice i meteora
        x2 = putanjaAsteroida[N_do_pogotka][0]
        y2 = putanjaAsteroida[N_do_pogotka][1]
        # postavljanje liste pozicija letjelice prije lansiranja
        lista = putanjaZemlje[:N_do_lansiranja+1]
        lista_r = []
        lista_x = []
        lista_y = []
        for r in lista:
            lista_r.append(np.array((r[0]+1000000, r[1]+1000000)))
            lista_x.append(r[0]+1000000)
            lista_y.append(r[1]+1000000)

        letjelica.r = lista_r
        letjelica.x = lista_x
        letjelica.y = lista_y
        # postavljanje početne brzine letjelice s obzirom na koordinate i udaljenost
        t = (N_do_pogotka-N_do_lansiranja)*self.dt
        s = np.sqrt((x2-x1)**2+(y2-y1)**2)
        v0 = s/t
        v0_kut = np.arctan2(y2-y1, x2-x1)
        v_x0 = v0*np.cos(v0_kut)
        v_y0 = v0*np.sin(v0_kut)
        letjelica.v.append(np.array((v_x0, v_y0)))
        print(f"brzina letjelice je: {np.sqrt(v_x0**2+v_y0**2)}")
        self.letjelica = letjelica

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
        uvjet_tijelo1 = self.__uvjet(x_collision, y_collision, x1_tijela1, x2_tijela1, y1_tijela1, y2_tijela1, tijelo1.rad, tijelo2.rad)
        uvjet_tijelo2 = self.__uvjet(x_collision, y_collision, x1_tijela2, x2_tijela2, y1_tijela2, y2_tijela2, tijelo1.rad, tijelo2.rad)
        if (uvjet_tijelo1 and uvjet_tijelo2):
            if(tijelo1.id=="letjelica" or tijelo2.id=="letjelica"):
                self.x_pogotka_letjelice = x_collision
                self.y_pogotka_letjelice = y_collision
            return True
        else:
            return False

    def __uvjet(self, x, y, x1, x2, y1, y2, r1, r2):
        # ova metoda provjerava nalazi li se sjecište (x, y) na dužini između točaka 1 i 2
        delta = (r1+r2)
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

    def applyGravity(self):
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
        # isključujemo gravitacijsko djelovanje za letjelicu
        if (tijelo.id == "letjelica"):
            return 0#*tijelo.v[-1]
        # računamo ukupnu akceleraciju na pojedini planet
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

    def __get_polar_coordinates(self, tijelo, i=-1):
        r0 = np.sqrt(tijelo.x[i]**2+tijelo.y[i]**2)
        r0_kut = np.arctan2(tijelo.y[i], tijelo.x[i])
        v0 = np.sqrt(np.dot(tijelo.v[i], tijelo.v[i]))
        v0_kut = np.arctan2(tijelo.v[i][1], tijelo.v[i][0])
        return r0, r0_kut, v0, v0_kut

    def __move_RungeKutta(self, tijelo, dt):
        self.currentPlanet = tijelo
        k1_v = self.__a_RK(tijelo.r[-1])*dt
        k1_r = tijelo.v[-1]*dt
        k2_v = self.__a_RK(tijelo.r[-1]+k1_r/2)*dt
        k2_r = (tijelo.v[-1]+k1_v/2)*dt
        k3_v = self.__a_RK(tijelo.r[-1]+k2_r/2)*dt
        k3_r = (tijelo.v[-1]+k2_v/2)*dt
        k4_v = self.__a_RK(tijelo.r[-1]+k3_r)*dt
        k4_r = (tijelo.v[-1]+k3_v)*dt
        tijelo.v.append(tijelo.v[-1]+(k1_v+2*k2_v+2*k3_v+k4_v)/6)
        tijelo.r.append(tijelo.r[-1]+(k1_r+2*k2_r+2*k3_r+k4_r)/6)
        tijelo.x.append(tijelo.r[-1][0])
        tijelo.y.append(tijelo.r[-1][1])

    def __a_RK(self, r_current):
        tijelo = self.currentPlanet
        # GRAVITACIJA NA PLANET
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
            G = 6.67*10**(-11) # newton-metre2-kilogram−2
            r12 = np.subtract(tijelo_i.r[-1], r_current)
            r = np.sqrt(np.dot(r12, r12))
            Fg_i = G*self.currentPlanet.mass*tijelo_i.mass/r**3 * r12 # vektor u smjeru planeta 2
            F_ukupna = np.add(F_ukupna, Fg_i)
        a = F_ukupna/tijelo.mass
        return a

    def resetSystem(self, i=0):
        self.time.clear()
        self.time.append(0)
        for tijelo in self.tijela:
            if (tijelo.id=="letjelica"):
                tijelo.r = []
                tijelo.v = []
                tijelo.a = []
                tijelo.x = []
                tijelo.y = []
            else:
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

    def clearLists(self):
        self.time = [0]
        for tijelo in self.tijela:
            tijelo.r = []
            tijelo.v = []
            tijelo.a = []
            tijelo.x = []
            tijelo.y = []
    
    def clear(self):
        self.time = [0]
        self.tijela = []

    def skiciraj(self, x1=-2*1.495978707*10**11, x2=2*1.495978707*10**11, y1=-2*1.495978707*10**11, y2=2*1.495978707*10**11):
        # fig = plt.figure()
        # plt.title('Graf')
        # plt.axis('equal')
        # plt.title("Sudar asteroida sa planetom")
        # plt.xlim(x1, x2)
        # plt.ylim(y1, y2)
        for tijelo in self.tijela:
            if (tijelo.id == "letjelica"):
                if(self.ZemljaPogodjenaBoolean):
                    plt.plot(tijelo.x, tijelo.y, label = tijelo.id, color = tijelo.color, linestyle='dotted')
                else:
                    plt.plot(tijelo.x, tijelo.y, label = tijelo.id, color = "red", linestyle='dotted')
                plt.scatter(tijelo.x[-1], tijelo.y[-1], color = tijelo.color, marker='*')
            else:
                plt.plot(tijelo.x, tijelo.y, label = tijelo.id, color = tijelo.color)
                plt.scatter(tijelo.x[-1], tijelo.y[-1], color=tijelo.color)
        if(self.x_pogotka_letjelice!=None and self.y_pogotka_letjelice!=None):
            plt.scatter(self.x_pogotka_letjelice, self.y_pogotka_letjelice, color="red", marker="X")
        # plt.show()

    def animiraj(self, x1=-2*1.496*10**11, x2=2*1.496*10**11, y1=-2*1.496*10**11, y2=2*1.496*10**11):
        self.xlim1 = x1
        self.xlim2 = x2
        self.ylim1 = y1
        self.ylim2 = y2
        fig = plt.figure()
        animation = ani.FuncAnimation(fig, self.animation_frame, len(self.time), interval=1, repeat=False)
        # writer = ani.PillowWriter(fps=60)
        # animation.save('animation.gif', writer='writer')
        plt.show()

    def animation_frame(self, i):
        plt.clf()
        plt.title("Sudar asteroida sa planetom")
        plt.axis('equal')
        plt.xlim(self.xlim1, self.xlim2)
        plt.ylim(self.ylim1, self.ylim2)
        for tijelo in self.tijela:
            if (tijelo.id == "letjelica"):
                if(self.ZemljaPogodjenaBoolean):
                    plt.plot(tijelo.x[:i], tijelo.y[:i], label = tijelo.id, color = tijelo.color, linestyle='dotted')
                else:
                    plt.plot(tijelo.x[:i], tijelo.y[:i], label = tijelo.id, color = "red", linestyle='dotted')
                plt.scatter(tijelo.x[i], tijelo.y[i], color = tijelo.color, marker='*')
            else:
                plt.plot(tijelo.x[:i], tijelo.y[:i], label = tijelo.id, color = tijelo.color)
                plt.scatter(tijelo.x[i], tijelo.y[i], color = tijelo.color)
        plt.legend()
        
    def getDistance(self, tijelo1, tijelo2):
        udaljenost = np.sqrt((tijelo1.x[-1]-tijelo2.x[-1])**2+(tijelo1.y[-1]-tijelo2.y[-1])**2)
        return udaljenost

    def getDistance2(self, r1, r2):
        udaljenost = np.sqrt((r2[0]-r1[0])**2+(r2[1]-r1[1])**2)
        return udaljenost

    def getMinimumDistance(self, tijelo1, tijelo2):
        min_value = self.getDistance2(tijelo1.r[0], tijelo2.r[0])
        for i in range(len(self.time)):
            value = self.getDistance2(tijelo1.r[i], tijelo2.r[i])
            if (value<min_value):
                min_value = value
        return min_value
