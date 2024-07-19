import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

# Konstante 
Km = 0.1
rw = 0.2
Iw = 0.5
rb = 0.02
mb = 10
Ra = 100
g = 0.5

#                                       sto je manji napon primecuje se vise kako se tocak vise zanosi zbog gravitacije svaki put kad je loptica pri vrhu
u = 30

sim_length = 1000

# Parametri izvuceni iz jednacina
a = -(2 * rw * Km**2) / (Ra * (7 * Iw + 2 * rw**2 * mb) * (rb + rw))
b = (g * (5 * Iw + 2 * rw**2 * mb)) / ((7 * Iw + 2 * rw**2 * mb) * (rb + rw))
c = (2 * rw * Km) / (Ra * (7 * Iw + 2 * rw**2 * mb) * (rb + rw))
p = - (7 * Km**2) / (Ra * (7 * Iw + 2 * rw**2 * mb))
q = (2 * g * rw * mb) / (7 * Iw + 2 * rw**2 * mb)
r = (7 * Km) / (Ra * (7 * Iw + 2 * rw**2 * mb))

assert np.isclose(a * r, c * p)

def f(x):
    return np.array([
        x[1],
        a * x[3] + b * np.sin(x[0]),
        x[3],
        p * x[3] + q * np.sin(x[0])
    ])

def g(x):
    return np.array([0, c, 0, r])

def dxdt(t, x):
    return f(x) + g(x) * u

# pocetni uslovi (polozaj loptice (ugao), brzina njenog kruznog kretanja, polozaj tocka (ugao), ugaona brzina rotacije tocka)
x0 = np.array([0.001, 2, 0, 0])
t_span = (0, 50)
t_eval = np.linspace(t_span[0], t_span[1], sim_length)
solution = solve_ivp(dxdt, t_span, x0, t_eval=t_eval)

t = solution.t
x1 = solution.y[0]
x3 = solution.y[2]

# Parametri krugova
r_tocak = 3
R_loptica = 1

fig, ax = plt.subplots()

circle_tocak = plt.Circle((0, 0), r_tocak, color='blue', fill=False)
ax.add_artist(circle_tocak)

circle_small = plt.Circle((0, 0), R_loptica, color='red', fill=False)
ax.add_artist(circle_small)

dot, = ax.plot([], [], 'ko', markersize=5)

# Postavi limite i proporcije
ax.set_xlim(-r_tocak - R_loptica - 1, r_tocak + R_loptica + 1)
ax.set_ylim(-r_tocak - R_loptica - 1, r_tocak + R_loptica + 1)
ax.set_aspect('equal', 'box')

def update(frame):
    # Ažuriraj koordinate manjeg kruga
    x1_current = x1[frame]
    x_small = (r_tocak + R_loptica) * np.sin(x1_current)
    y_small = (r_tocak + R_loptica) * np.cos(x1_current)
    circle_small.center = (x_small, y_small)
    
    # koordinate crne tačkice, da se pokaze rotacija tocka
    x3_current = x3[frame]
    x_dot = r_tocak * np.sin(x3_current)
    y_dot = r_tocak * np.cos(x3_current)
    dot.set_data(x_dot, y_dot)
    
    return circle_small, dot


ani = animation.FuncAnimation(fig, update, frames=len(t), interval=1000/30, blit=True)


plt.grid(True)
plt.show()
