import numpy as np
import matplotlib.pyplot as plt
import control 
from control.matlab import *

Km = 0.1
rw = 0.2
Iw = 0.5
rb = 0.02
mb = 10
Ra = 100
g = 9.81
u = 10000

s = tf("s")

G = 1/((Iw*s + Km**2/Ra)*Ra/Km)

y, T = step(G, 100000)

plt
plt.plot(T, y)
plt.show()