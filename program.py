from tijelo import Tijelo
from svemir import Sustav
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np

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

masaJupitra =  1.898 * 10**27 #kg
radijusJupitra = 6.9911 * 10**7 #m
udaljenostJupitra = 7.786*10**11 #m
brzinaJupitra =1.31*10**4 #m/s

masaSaturna = 5.683 * 10**26 #kg
radijusSaturna = 5.8232 * 10**7 #m
udaljenostSaturna = 1.4335*10**12 #m
brzinaSaturna = 9.7 *10**3 #m/s

masaUrana = 8.681 * 10**25 #kg
radijusUrana = 2.5362 * 10**7 #m
udaljenostUrana = 2.8725*10**12 #m
brzinaUrana =  6.8*10**3 #m/s

masaNeptuna = 1.024 * 10**26 #kg
radijusNeptuna = 2.4622 * 10**7 #m
udaljenostNeptuna = 4.4951*10**12 #m
brzinaNeptuna = 5.4*10**3 #m/s

masaAsteroida = 5.27*10**10 #kg
radijusAsteroida = 390 #m
udaljenostAsteroida = 4*udaljenostZemlje # a.u.
brzinaAsteroidaPriUdaru = 5.8*10**4 #m/s
kutBrzineAsteroidaPriUdaru = 310 # stupnjeva

masaLetjelice = 610 #kg
radijusLetjelice = 2 #m

# planeti
Sunce = Tijelo(masaSunca, radijusSunca, "Sunce")
Merkur = Tijelo(masaMerkura, radijusMerkura, "Merkur")
Venera = Tijelo(masaVenere, radijusVenere, "Venera")
Zemlja = Tijelo(masaZemlje, radijusZemlje, "Zemlja")
Mars = Tijelo(masaMarsa, radijusMarsa, "Mars")
Jupiter = Tijelo(masaJupitra, radijusJupitra, "Jupiter")
Saturn = Tijelo(masaSaturna, radijusSaturna, "Saturn")
Uran = Tijelo(masaUrana, radijusUrana, "Uran")
Neptun = Tijelo(masaNeptuna, radijusNeptuna, "Neptun")

# asteroid
Asteroid = Tijelo(masaAsteroida, radijusAsteroida, "asteroid")

# dodajemo planete sa uvjetima u trenutku sudara asteroida sa Zemljom
SuncevSustav.addPlanet(Sunce, 0, 0, 0, 90)
SuncevSustav.addPlanet(Merkur, udaljenostMerkura, 0, brzinaMerkura, 90)
SuncevSustav.addPlanet(Venera, udaljenostVenere, 0, brzinaVenere, 90)
SuncevSustav.addPlanet(Zemlja, udaljenostZemlje, 0, brzinaZemlje, 90)
SuncevSustav.addPlanet(Mars, udaljenostMarsa, 0, brzinaMarsa, 90)
SuncevSustav.addPlanet(Jupiter, udaljenostJupitra, 0, brzinaJupitra, 90)
SuncevSustav.addPlanet(Saturn, udaljenostSaturna, 0, brzinaSaturna, 90)
SuncevSustav.addPlanet(Uran, udaljenostUrana, 0, brzinaUrana, 90)
SuncevSustav.addPlanet(Neptun, udaljenostNeptuna, 0, brzinaNeptuna, 90)
SuncevSustav.shootComet(Asteroid, udaljenostZemlje+radijusZemlje, 0, brzinaAsteroidaPriUdaru, kutBrzineAsteroidaPriUdaru)

# letjelica
Letjelica = Tijelo(masaLetjelice, radijusLetjelice, "letjelica")

# reverse
SuncevSustav.reverseEvolve()

putanjaAsteroida = Asteroid.r
putanjaZemlje = Zemlja.r

SuncevSustav.resetSystem(-1) # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
SuncevSustav.launch(Letjelica, putanjaAsteroida, putanjaZemlje, N_do_trenutka_pogotka=10)
SuncevSustav.evolve()

fig = plt.figure()
plt.title('Graf')
plt.axis('equal')
plt.title("Sudar asteroida sa planetom")

# SKICA
# plt.xlim(udaljenostZemlje-10000000000, udaljenostZemlje+10000000000)
# plt.ylim(-10000000000, 10000000000)
# plt.scatter(Sunce.x, Sunce.y, color="yellow", label="Sunce")
# plt.scatter(Merkur.x, Merkur.y, color="brown", label="Merkur")
# plt.scatter(Venera.x, Venera.y, color="orange", label="Venera")
# plt.scatter(Zemlja.x, Zemlja.y, color="blue", label="Zemlja")
# plt.scatter(Mars.x, Mars.y, color="green", label="Mars")
# plt.scatter(Asteroid.x, Asteroid.y, color="black", label="asteroid")        
# plt.scatter(Letjelica.x, Letjelica.y, color="darkblue")

# ANIMACIJA
def animation_frame(i):
    try:
        plt.clf()
        plt.axis('equal')
        plt.xlim(-2*udaljenostZemlje, 2*udaljenostZemlje)
        plt.ylim(-2*udaljenostZemlje, 2*udaljenostZemlje)
        plt.plot(Sunce.x[:i], Sunce.y[:i], label = "Sunce", color = "yellow")
        plt.plot(Merkur.x[:i], Merkur.y[:i], label = "Merkur", color = "brown")
        plt.plot(Venera.x[:i], Venera.y[:i], label = "Venera", color = "orange")
        plt.plot(Zemlja.x[:i], Zemlja.y[:i], label = "Zemlja", color = "blue")
        plt.plot(Mars.x[:i], Mars.y[:i], label = "Mars", color = "green")
        plt.plot(Jupiter.x[:i], Jupiter.y[:i], label = "Jupiter", color = "pink")
        plt.plot(Saturn.x[:i], Saturn.y[:i], label = "Saturn", color = "purple")
        plt.plot(Uran.x[:i], Uran.y[:i], label = "Uran", color = "lightslategrey")
        plt.plot(Neptun.x[:i], Neptun.y[:i], label = "Neptun", color = "darkslateblue")
        plt.plot(Asteroid.x[:i], Asteroid.y[:i], label = "asteroid", color = "black")
        plt.plot(Letjelica.x[:i], Letjelica.y[:i], label = "letjelica", color = "darkblue")
        plt.scatter(Sunce.x[i], Sunce.y[i], color="yellow")
        plt.scatter(Merkur.x[i], Merkur.y[i], color="brown")
        plt.scatter(Venera.x[i], Venera.y[i], color="orange")
        plt.scatter(Zemlja.x[i], Zemlja.y[i], color="blue")
        plt.scatter(Mars.x[i], Mars.y[i], color="green")
        plt.scatter(Jupiter.x[i], Jupiter.y[i], color="pink")
        plt.scatter(Saturn.x[i], Saturn.y[i], color="purple")
        plt.scatter(Uran.x[i], Uran.y[i], color="lightslategrey")
        plt.scatter(Neptun.x[i], Neptun.y[i], color="darkslateblue")
        plt.scatter(Asteroid.x[i], Asteroid.y[i], color="black")
        plt.scatter(Letjelica.x[i], Letjelica.y[i], label = "letjelica", color = "darkblue", marker="^")
        plt.legend()
    except:
        plt.scatter(Sunce.x[-1], Sunce.y[-1], color="yellow")
        plt.scatter(Merkur.x[-1], Merkur.y[-1], color="brown")
        plt.scatter(Venera.x[-1], Venera.y[-1], color="orange")
        plt.scatter(Zemlja.x[-1], Zemlja.y[-1], color="blue")
        plt.scatter(Mars.x[-1], Mars.y[-1], color="green")
        plt.scatter(Jupiter.x[-1], Jupiter.y[-1], color="pink")
        plt.scatter(Saturn.x[-1], Saturn.y[-1], color="purple")
        plt.scatter(Uran.x[-1], Uran.y[-1], color="lightslategrey")
        plt.scatter(Neptun.x[-1], Neptun.y[-1], color="darkslateblue")
        plt.scatter(Asteroid.x[-1], Asteroid.y[-1], color="black")
        plt.scatter(Letjelica.x[-1], Letjelica.y[-1], color="darkblue", marker="^")
        plt.legend()
        pass

animation = ani.FuncAnimation(fig, animation_frame, 2000, interval=1)
plt.show()
writer = ani.PillowWriter(fps=60)
animation.save('./udar_asteroida.gif', writer='writer')

