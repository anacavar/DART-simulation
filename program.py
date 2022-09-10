from tijelo import Tijelo
from svemir import Sustav
import matplotlib.pyplot as plt
import numpy as np
np.seterr(all='raise')

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
# kutBrzineAsteroidaPriUdaru = 270 # stupnjeva --
# kutBrzineAsteroidaPriUdaru = 200 # stupnjeva ++

masaLetjelice = 610 #kg
radijusLetjelice = 2 #m

# planeti
Sunce = Tijelo(masaSunca, radijusSunca, "Sunce", "yellow")
Merkur = Tijelo(masaMerkura, radijusMerkura, "Merkur", "brown")
Venera = Tijelo(masaVenere, radijusVenere, "Venera", "orange")
Zemlja = Tijelo(masaZemlje, radijusZemlje, "Zemlja", "blue")
Mars = Tijelo(masaMarsa, radijusMarsa, "Mars", "green")
Jupiter = Tijelo(masaJupitra, radijusJupitra, "Jupiter", "pink")
Saturn = Tijelo(masaSaturna, radijusSaturna, "Saturn", "purple")
Uran = Tijelo(masaUrana, radijusUrana, "Uran", "lightslategrey")
Neptun = Tijelo(masaNeptuna, radijusNeptuna, "Neptun", "darkslategrey")

# asteroid
Asteroid = Tijelo(masaAsteroida, radijusAsteroida, "asteroid", "black")

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
Letjelica = Tijelo(masaLetjelice, radijusLetjelice, "letjelica", "darkblue")

# prije gibanja postavimo odnose gravitacijskih sila na tijela
SuncevSustav.applyGravity()

# negativna, pa pozitivna evolucija
SuncevSustav.reverseEvolve()
putanjaAsteroida = Asteroid.r
putanjaZemlje = Zemlja.r

SuncevSustav.resetSystem(-1) # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
SuncevSustav.evolve()

# uzmi putanje Zemlje i asteroida
putanjaAsteroida = []
putanjaZemlje = []
for r in Asteroid.r:
  putanjaAsteroida.append(r)
for r in Zemlja.r:
  putanjaZemlje.append(r)

SuncevSustav.tijela.append(Letjelica)

# 1. STUDIJA - jednu točku putanje asteroida gađamo iz svake točke putanje Zemlje

# fig = plt.figure()
# plt.title('Graf')
# plt.axis('equal')
# plt.title("Sudar asteroida sa planetom")
# plt.xlim(-2*udaljenostZemlje, 2*udaljenostZemlje)
# plt.ylim(-2*udaljenostZemlje, 2*udaljenostZemlje)


# for i in range(20):
#   print(f"Vrtnja {i}")
#   SuncevSustav.resetSystem() # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
#   SuncevSustav.launch(Letjelica, putanjaAsteroida, putanjaZemlje, N_do_lansiranja=i, N_do_pogotka=50)
#   SuncevSustav.evolve()
#   SuncevSustav.skiciraj()
#   # print(f"broj letjelica: {len(Letjelica.r)}")
#   # print(f"broj zemalja: {len(Zemlja.r)}")
#   # SuncevSustav.animiraj()

# plt.show()

# 2. STUDIJA - svaku točku putanje asteroida gađamo iz jedne točke putanje Zemlje

fig = plt.figure()
plt.title('Graf')
plt.axis('equal')
plt.title("Sudar asteroida sa planetom")
plt.xlim(-2*udaljenostZemlje, 2*udaljenostZemlje)
plt.ylim(-2*udaljenostZemlje, 2*udaljenostZemlje)

for i in range(12, 50):
  print(f"Vrtnja {i}")
  SuncevSustav.resetSystem() # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
  SuncevSustav.launch(Letjelica, putanjaAsteroida, putanjaZemlje, N_do_lansiranja=10, N_do_pogotka=i)
  SuncevSustav.evolve()
  SuncevSustav.skiciraj()
  # SuncevSustav.animiraj()

plt.show()