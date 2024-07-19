import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
Km = 0.1
rw = 0.2
Iw = 0.5
rb = 0.02
mb = 10
Ra = 100
g = 0.5
u = 0

sim_length = 100

# Parameters
a = -(2 * rw * Km**2) / (Ra * (7 * Iw + 2 * rw**2 * mb) * (rb + rw))
b = (g * (5 * Iw + 2 * rw**2 * mb)) / ((7 * Iw + 2 * rw**2 * mb) * (rb + rw))
c = (2 * rw * Km) / (Ra * (7 * Iw + 2 * rw**2 * mb) * (rb + rw))
p = - (7 * Km**2) / (Ra * (7 * Iw + 2 * rw**2 * mb))
q = (2 * g * rw * mb) / (7 * Iw + 2 * rw**2 * mb)
r = (7 * Km) / (Ra * (7 * Iw + 2 * rw**2 * mb))

assert np.isclose(a * r, c * p)

# Functions
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

# Initial conditions
x0 = np.array([0.001, 2, 0, 0])

#                                REFERENCA DVADESET DEVET!!!!

# Time span
t_span = (0, 50)
t_eval = np.linspace(t_span[0], t_span[1], sim_length)

# Solve the system
solution = solve_ivp(dxdt, t_span, x0, t_eval=t_eval)

# Results
t = solution.t
x1 = solution.y[0]
x2 = solution.y[1]
x3 = solution.y[2]
x4 = solution.y[3]

# Animation
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True)

# Vectors
short_vector, = ax.plot([], [], 'r-', lw=2, label='Short Vector')
long_vector, = ax.plot([], [], 'b-', lw=2, label='Long Vector')

# Annotations
text_x1 = ax.text(0.05, 0.95, '', transform=ax.transAxes)
text_x2 = ax.text(0.05, 0.90, '', transform=ax.transAxes)
text_x3 = ax.text(0.05, 0.85, '', transform=ax.transAxes)
text_x4 = ax.text(0.05, 0.80, '', transform=ax.transAxes)

# Initialize animation
def init():
    short_vector.set_data([], [])
    long_vector.set_data([], [])
    text_x1.set_text('')
    text_x2.set_text('')
    text_x3.set_text('')
    text_x4.set_text('')
    return short_vector, long_vector, text_x1, text_x2, text_x3, text_x4

# Update function for animation
def update(frame):
    angle_short = x1[frame] + np.pi / 2
    angle_long = x3[frame] + np.pi / 2
    
    short_x = np.cos(angle_short)
    short_y = np.sin(angle_short)
    
    long_x = np.cos(angle_long)
    long_y = np.sin(angle_long)
    
    short_vector.set_data([0, short_x], [0, short_y])
    long_vector.set_data([0, long_x], [0, long_y])
    
    text_x1.set_text(f'x1 = {x1[frame]:.2f}')
    text_x2.set_text(f'x2 = {x2[frame]:.2f}')
    text_x3.set_text(f'x3 = {x3[frame]:.2f}')
    text_x4.set_text(f'x4 = {x4[frame]:.2f}')
    
    return short_vector, long_vector, text_x1, text_x2, text_x3, text_x4

# Create animation
ani = animation.FuncAnimation(fig, update, frames=sim_length, init_func=init, blit=True)

ax.legend()

plt.show()

