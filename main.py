import numpy as np

from viewer import Viewer
from colony import Colony

colony = Colony((100, 100), (50, 50))
colony.spawn_food(circle=(400//6, 500//6, 50//6))
colony.spawn_ant(amount=50)

def next_frame():
    colony.next_frame()
    return colony.render()

viewer = Viewer(next_frame, (600, 600), frames_per_sec=10)
viewer.start()