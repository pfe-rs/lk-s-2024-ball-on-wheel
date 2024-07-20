import matplotlib.pyplot as plt

def animacija(r_tocak, R_loptica):
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

               def update(frame, x1):
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
