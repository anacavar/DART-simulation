from tijelo import Tijelo
from svemir import Sustav
import matplotlib.pyplot as plt
import matplotlib.animation as ani

SuncevSustav = Sustav()

# PODACI O PLANETIMA
masaSunca = 1.989 * 10**30 #kg
radijusSunca = 6.96340 * 10**8 #m

masaMerkura = 3.285 * 10**23 #kg
radijusMerkura = 2.4397 * 10**6 #m
udaljenostMerkura = 5.79*10**10  #m
brzinaMerkura = 4.79*10**4 #m/s

masaVenere = 4.867 * 10**24 #kg
radijusVenere = 6.0518 * 10**6 #m
udaljenostVenere =  1.082*10**11 #m
brzinaVenere = 3.50*10**4 #m/s

masaZemlje = 5.972 * 10**24 #kg
radijusZemlje = 6.371 * 10**6 #m
udaljenostZemlje = 1.496*10**11 #m
brzinaZemlje = 2.98 * 10**4 #m/s

masaMarsa = 6.39 * 10**23 #kg
radijusMarsa = 3.3895 * 10**6 #m
udaljenostMarsa = 2.279*10**11 #m
brzinaMarsa = 2.41*10**4 #m/s

masaKometa = 1014 #kg
radijusKometa = 10*10**3 #m
udaljenostKometa = 4*udaljenostZemlje # a.u.
brzinaKometaPriUdaru = 4.8*10**4 #m/s
kutBrzineKometaPriUdaru = 30 # stupnjeva

# planeti
Sunce = Tijelo(masaSunca, radijusSunca)
Merkur = Tijelo(masaMerkura, radijusMerkura)
Venera = Tijelo(masaVenere, radijusVenere)
Zemlja = Tijelo(masaZemlje, radijusZemlje)
Mars = Tijelo(masaMarsa, radijusMarsa)

#komet
Komet = Tijelo(masaKometa, radijusKometa)

#dodajemo planete sa uvjetima u trenutku sudara kometa sa Zemljom
SuncevSustav.addPlanet(Sunce, 0, 0, 0, 90)
SuncevSustav.addPlanet(Merkur, udaljenostMerkura, 0, brzinaMerkura, 90)
SuncevSustav.addPlanet(Venera, udaljenostVenere, 0, brzinaVenere, 90)
SuncevSustav.addPlanet(Zemlja, udaljenostZemlje, 0, brzinaZemlje, 90)
SuncevSustav.addPlanet(Mars, udaljenostMarsa, 0, brzinaMarsa, 90)
SuncevSustav.shootComet(Komet, udaljenostZemlje+radijusZemlje, 0, brzinaKometaPriUdaru, kutBrzineKometaPriUdaru)

#reverse
SuncevSustav.reverseEvolve()
SuncevSustav.resetSystem(-1) #postavlja sva tijela na početne uvjete kako bi došlo do sudara kometa sa Zemljom
SuncevSustav.evolve()

fig = plt.figure()
plt.title('Graf')
plt.axis('equal')

# ANIMACIJA
def animation_frame(i):
    try:
        plt.clf()
        plt.axis('equal')
        plt.xlim(-4*udaljenostZemlje, 4*udaljenostZemlje)
        plt.ylim(-4*udaljenostZemlje, 4*udaljenostZemlje)
        plt.plot(Sunce.x[:i], Sunce.y[:i], label = "Sunce", color = "yellow")
        plt.plot(Merkur.x[:i], Merkur.y[:i], label = "Merkur", color = "brown")
        plt.plot(Venera.x[:i], Venera.y[:i], label = "Venera", color = "orange")
        plt.plot(Zemlja.x[:i], Zemlja.y[:i], label = "Zemlja", color = "blue")
        plt.plot(Mars.x[:i], Mars.y[:i], label = "Mars", color = "green")
        plt.plot(Komet.x[:i], Komet.y[:i], label = "komet", color = "black")
        plt.scatter(Sunce.x[i], Sunce.y[i], color="yellow")
        plt.scatter(Merkur.x[i], Merkur.y[i], color="brown")
        plt.scatter(Venera.x[i], Venera.y[i], color="orange")
        plt.scatter(Zemlja.x[i], Zemlja.y[i], color="blue")
        plt.scatter(Mars.x[i], Mars.y[i], color="green")
        plt.scatter(Komet.x[i], Komet.y[i], color="black")
        plt.legend()
    except:
        plt.scatter(Sunce.x[-1], Sunce.y[-1], color="yellow")
        plt.scatter(Merkur.x[-1], Merkur.y[-1], color="brown")
        plt.scatter(Venera.x[-1], Venera.y[-1], color="orange")
        plt.scatter(Zemlja.x[-1], Zemlja.y[-1], color="blue")
        plt.scatter(Mars.x[-1], Mars.y[-1], color="green")
        plt.scatter(Komet.x[-1], Komet.y[-1], color="black")
        pass

animator = ani.FuncAnimation(fig, animation_frame, 2000, interval=1)

plt.title("Sudar kometa sa planetom")
plt.show()