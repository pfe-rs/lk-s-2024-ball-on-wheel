import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp
import animacija

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

animacija.animacija(r_tocak, R_loptica, t, x1, x3)
