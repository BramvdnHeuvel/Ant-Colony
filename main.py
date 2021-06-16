import numpy as np

from viewer import Viewer
from colony import Colony

# CONSTANTS
PIXEL_SIZE = 2
ANT_INTENSITY = 250
MAX_INTENSITY = 1000

# GAME RULES
WIDTH = 500
HEIGHT = 500
COLONY_X = 250
COLONY_Y = 250


colony = Colony(
    size=(WIDTH, HEIGHT), 
    location=(COLONY_X, COLONY_Y), 
    intensity_per_ant=ANT_INTENSITY,
    intensity_max=MAX_INTENSITY
)

#colony.spawn_food(circle=(175, 175, 25))
colony.spawn_ant(amount=500)

def next_frame():
    """Render the next frame"""
    colony.next_frame()
    return colony.render(PIXEL_SIZE)

def on_mouse_down(x, y):
    """Perform action when the user clicks on the given location"""
    colony.spawn_food(circle=(x, y, 50))

# Start showing the ant colony simulation
viewer = Viewer(
    display_size=(WIDTH, HEIGHT), 
    update_func=next_frame, 
    pixel_size=PIXEL_SIZE,
    on_mouse_down=on_mouse_down,
    frames_per_sec=30
)
viewer.start()