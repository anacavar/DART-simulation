from planet import Planet
from svemir import Sustav
import matplotlib.pyplot as plt
import matplotlib.animation as ani

Sunce = Planet(1000, 0, 0)
Zemlja = Planet(1, 10, 10)

SuncevSustav = Sustav(Sunce)
SuncevSustav.addPlanet(Zemlja)
SuncevSustav.evolve()

fig = plt.figure()
plt.title('Graf')

def animation_frame(i):
    plt.scatter(Sunce.x[:i], Sunce.y[:i], color = 'blue')
    plt.plot(Zemlja.x[:i], Zemlja.y[:i], color = 'red')

animator = ani.FuncAnimation(fig, animation_frame, 2000)

plt.show()


