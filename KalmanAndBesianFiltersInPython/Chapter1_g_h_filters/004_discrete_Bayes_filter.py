__author__ = 'Maxiee'

import numpy as np
import matplotlib.pyplot as plt
import utils.book_plots as bp

def update(pos_belief, measure, p_hit, p_miss):
    for i in range(len(hallway)):
        if hallway[i] == measure:
            pos_belief[i] *= p_hit
        else:
            pos_belief[i] *= p_miss
    pos_belief /= sum(pos_belief)


def predict(pos_belief, move, p_correct, p_under, p_over):
    n = len(pos_belief)
    result = np.zeros(n)
    for i in range(n):
        result[i] = (
            pos_belief[(i-move) % n] * p_correct +
            pos_belief[(i-move-1) %n] * p_over +
            pos_belief[(i-move+1) %n] * p_under
        )
    pos_belief[:] = result

pos_belief = np.array([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])

hallway = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])

# pos_belief = np.array([0.2]*10)
# reading = 1

# pos_belief = np.array([0, 0, .4, .6, 0, 0, 0, 0, 0, 0], dtype=float)

update(pos_belief, 1, .6, .2)
print(pos_belief)
bp.bar_plot(pos_belief)
plt.show()

predict(pos_belief, 1, .8, .1, .1)
print(pos_belief)
bp.bar_plot(pos_belief)
plt.show()

update(pos_belief, 1, .6, .2)
print(pos_belief)
bp.bar_plot(pos_belief)
plt.show()

predict(pos_belief, 1, .8, .1, .1)
print(pos_belief)
bp.bar_plot(pos_belief)
plt.show()

update(pos_belief, 0, .6, .2)
print(pos_belief)
bp.bar_plot(pos_belief)
plt.show()

predict(pos_belief, 1, .8, .1, .1)
print(pos_belief)
bp.bar_plot(pos_belief)
plt.show()

update(pos_belief, 0, .6, .2)
print(pos_belief)
bp.bar_plot(pos_belief)
plt.show()