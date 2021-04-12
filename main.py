import numpy as np

from viewer import Viewer
from colony import Colony

# CONSTANTS
PIXEL_SIZE = 18
MAX_INTENSITY = 250

# GAME RULES
WIDTH = 50
HEIGHT = 50
COLONY_X = 25
COLONY_Y = 25


colony = Colony((WIDTH, HEIGHT), (COLONY_X, COLONY_Y), intensity=MAX_INTENSITY)
#colony.spawn_food(circle=(175, 175, 25))
colony.spawn_ant(amount=5)

def next_frame():
    colony.next_frame()
    return colony.render(PIXEL_SIZE)

def on_mouse_down(x, y):
    colony.spawn_food(circle=(x, y, 5))

# Start showing the ant colony simulation
viewer = Viewer(
    display_size=(WIDTH, HEIGHT), 
    update_func=next_frame, 
    pixel_size=PIXEL_SIZE,
    on_mouse_down=on_mouse_down,
    frames_per_sec=15
)
viewer.start()