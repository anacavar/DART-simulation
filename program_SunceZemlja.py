from planet import Planet
from svemir import Sustav
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# masa sunca 1.989 × 10^30 kg, 
# masa zemlje 5.972 × 10^24 kg
# zemlja sunce perihelion 147.3 *1000000 * 1000 metara
# brzina zemlje na perihelionu 30.29 km/s = 30290 m/s

Sunce = Planet(1.989*10**30, 0, 0)
Zemlja = Planet(5.972*10**24, 147.3*10**9, 30290)

SuncevSustav = Sustav(Sunce)
SuncevSustav.addPlanet(Zemlja)
SuncevSustav.evolve1()

fig = plt.figure()
plt.title('Graf')

#ANIMACIJA
# def animation_frame(i):
#     plt.scatter(Sunce.x[:i], Sunce.y[:i], color = 'blue')
#     plt.plot(Zemlja.x[:i], Zemlja.y[:i], color = 'red')

# animator = ani.FuncAnimation(fig, animation_frame, 2000)

plt.plot(Zemlja.x, Zemlja.y)
plt.scatter(Sunce.x, Sunce.y)
plt.show()


