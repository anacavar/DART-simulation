from tijelo import Tijelo
from svemir import Sustav
import matplotlib.pyplot as plt
import numpy as np
np.seterr(all='raise')

SuncevSustav = Sustav()


DT = 60*60*24/10 ####################################################################VARIJABLA KOJU MIJENJAMO

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

masaAsteroida = 5.27*10**8 #kg
radijusAsteroida = 390 #m
udaljenostAsteroida = 6*udaljenostZemlje # a.u. ###################################################MIJENJAMO
brzinaAsteroidaPriUdaru = 4*10**4 #5.8*10**4 #m/s #################################################VARIJABLA KOJU MIJENJAMO
kutBrzineAsteroidaPriUdaru = 310 # stupnjeva ++ check
# kutBrzineAsteroidaPriUdaru = 210 # stupnjeva ++ check
# kutBrzineAsteroidaPriUdaru = 20 #10 # stupnjeva ++ check
# kutBrzineAsteroidaPriUdaru = 110 # stupnjeva ++ check

masaLetjelice = 610*5 #kg
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
SuncevSustav.shootComet(Asteroid, udaljenostZemlje+5*radijusZemlje/10, 0, brzinaAsteroidaPriUdaru, kutBrzineAsteroidaPriUdaru)

# letjelica
Letjelica = Tijelo(masaLetjelice, radijusLetjelice, "letjelica", "darkblue")

# prije gibanja postavimo odnose gravitacijskih sila na tijela
SuncevSustav.applyGravity()

# negativna, pa pozitivna evolucija
SuncevSustav.reverseEvolve(dt=DT, max_distance=udaljenostAsteroida)
putanjaAsteroida = Asteroid.r
putanjaZemlje = Zemlja.r

SuncevSustav.resetSystem(-1) # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
SuncevSustav.evolve(dt=DT)

# Jednostavna evolucija

# SuncevSustav.reverseEvolve(dt=DT, max_distance=udaljenostAsteroida)
# SuncevSustav.resetSystem(-1) # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
# SuncevSustav.evolve(dt=DT)
# # SuncevSustav.resetSystem()
# # SuncevSustav.launch()
# # SuncevSustav.evolve(dt = DT)

# fig = plt.figure()
# plt.title('Graf')
# plt.axis('equal')
# plt.title("Sudar asteroida sa planetom")
# plt.xlim(-2*udaljenostZemlje, 2*udaljenostZemlje)
# plt.ylim(-2*udaljenostZemlje, 2*udaljenostZemlje)
# plt.xlabel("x/m")
# plt.ylabel("y/m")
# SuncevSustav.skiciraj()
# # plt.savefig('skica1.png')
# plt.show()

# min = SuncevSustav.getMinimumDistance(Zemlja, Asteroid)
# print(min/radijusZemlje)

# print(SuncevSustav.getDistance2(Zemlja.r[-1], Asteroid.r[-1])/radijusZemlje)

# uzmi putanje Zemlje i asteroida
putanjaAsteroida = []
putanjaZemlje = []
for r in Asteroid.r:
  putanjaAsteroida.append(r)
for r in Zemlja.r:
  putanjaZemlje.append(r)

SuncevSustav.tijela.append(Letjelica)

N_ukupno = len(SuncevSustav.time)

print(f"Ukupan broj koraka: {N_ukupno}")

# # 1. STUDIJA - jednu točku putanje asteroida gađamo iz svake točke putanje Zemlje

# fig = plt.figure()
# plt.axis('equal')
# plt.title("Sudar asteroida sa planetom")
# plt.xlim(-2*udaljenostZemlje, 2*udaljenostZemlje)
# plt.ylim(-5*udaljenostZemlje, 2*udaljenostZemlje)

# indeksi_lista = []
# udaljenosti_lista = []

# for i in range(400, 2500, 100):
#   print(f"Vrtnja {i}")
#   indeksi_lista.append(i)
#   SuncevSustav.resetSystem() # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
#   SuncevSustav.launch(Letjelica, putanjaAsteroida, putanjaZemlje, N_do_lansiranja=i, N_do_pogotka=3900)
#   SuncevSustav.evolve(dt = DT)
#   SuncevSustav.skiciraj()
#   # SuncevSustav.animiraj()
#   min = SuncevSustav.getMinimumDistance(Zemlja, Asteroid)
#   print(f"Udaljenost je: {min/radijusZemlje}")
#   udaljenosti_lista.append(min/radijusZemlje)

# plt.savefig("study1.png")
# plt.show()

# fig = plt.figure()
# plt.title("Ovisnost minimalne udaljenosti asteroida i Zemlje o točki polijetanja letjelice")
# plt.plot(indeksi_lista, udaljenosti_lista)
# y = []
# for i in indeksi_lista:
#   y.append(1)
# plt.plot(indeksi_lista, y, color="red", linestyle="dashed")
# plt.xlabel('i_Zemlje')
# plt.ylabel('d_min / rad_Z')
# plt.savefig("graf-study1.png")
# plt.show()


# # 2. STUDIJA - svaku točku putanje asteroida gađamo iz jedne točke putanje Zemlje

fig = plt.figure()
plt.axis('equal')
plt.title("Gađanje asteroida letjelicom")
plt.xlim(-2*udaljenostZemlje, 2*udaljenostZemlje)
plt.ylim(-5*udaljenostZemlje, 2*udaljenostZemlje)
plt.xlabel('x/m')
plt.ylabel('y/m')

indeksi_lista = []
udaljenosti_lista = []

for i in range(1600, 5000, 100):
  print(f"Vrtnja {i}")
  indeksi_lista.append(i)
  SuncevSustav.resetSystem() # postavlja sva tijela na početne uvjete kako bi došlo do sudara asteroida sa Zemljom
  SuncevSustav.launch(Letjelica, putanjaAsteroida, putanjaZemlje, N_do_lansiranja=500, N_do_pogotka=i)
  SuncevSustav.evolve(dt = DT)
  SuncevSustav.skiciraj()
  # SuncevSustav.animiraj()
  min = SuncevSustav.getMinimumDistance(Zemlja, Asteroid)
  print(f"Udaljenost je: {min/radijusZemlje}")
  udaljenosti_lista.append(min/radijusZemlje)

plt.savefig("study2.png")
plt.legend()
plt.show()

fig = plt.figure()
# plt.axis('equal')
plt.title("Ovisnost minimalne udaljenosti asteroida i Zemlje o točki udara letjelice")
plt.plot(indeksi_lista, udaljenosti_lista)
y = []
for i in indeksi_lista:
  y.append(1)
plt.plot(indeksi_lista, y, color="red", linestyle="dashed")
plt.xlabel('i_Zemlje')
plt.ylabel('d_min / rad_Z')
plt.savefig("graf-study2.png")
plt.show()

