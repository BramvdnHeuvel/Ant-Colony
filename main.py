import numpy as np

from viewer import Viewer
from colony import Colony

# CONSTANTS
PIXEL_SIZE = 4
MAX_INTENSITY = 10

# GAME RULES
WIDTH = 250
HEIGHT = 250
COLONY_X = 125
COLONY_Y = 125


colony = Colony((WIDTH, HEIGHT), (COLONY_X, COLONY_Y), intensity=MAX_INTENSITY)
colony.spawn_food(circle=(200, 200, 25))
colony.spawn_ant(amount=500)

def next_frame():
    colony.next_frame()
    return colony.render(PIXEL_SIZE)

# Start showing the ant colony simulation
viewer = Viewer(next_frame, 
    (PIXEL_SIZE*WIDTH, PIXEL_SIZE*HEIGHT), 
    frames_per_sec=10
)
viewer.start()