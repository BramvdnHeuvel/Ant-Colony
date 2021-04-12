from typing import Tuple, Optional
from ant import Ant
import random
import numpy

class Colony:
    def __init__(self, 
        size : Tuple[int, int], 
        location : Tuple[int, int],
        intensity : Optional[int]
        ):
        self.size = size
        self.origin = location

        # Local variables
        self.scent = {}
        self.food = set()
        self.ants = []

        # Constants
        self.MAX_SCENT_INTENSITY = intensity

    def next_frame(self):
        """Simulate the next frame for the ant colony"""
        for ant in self.ants:
            x, y = ant.move(self.scent, self.size)

            # Hungry ant finds food
            if (x, y) in self.food and ant.state == 'HUNGRY':
                ant.change_state('FULL')
                self.food.remove((x, y))
            
            # Ant with food arrives at the colony
            if (x, y) == self.origin and ant.state == 'FULL':
                ant.change_state('HUNGRY')

                if random.random() < 0.5:
                    self.spawn_ant()
        
        self.__decay_scent()

    def render(self, pixel_size : int):
        """Show the colony's current state"""
        view = numpy.ndarray((*self.size, 3)) * 0

        # Show scents
        for x in self.scent:
            for y in self.scent[x]:
                for z in self.scent[x][y]:
                    if z == 'HUNGRY':
                        view[x, y, 2] = int(
                            255 * self.scent[x][y][z] / self.MAX_SCENT_INTENSITY
                        )
                    if z == 'FULL':
                        view[x, y, 0] = int(
                            255 * self.scent[x][y][z] / self.MAX_SCENT_INTENSITY
                        )
        
        # Show food
        for pixel in self.food:
            x, y = pixel
            view[x, y, 1] = 255
        
        # Show ants
        for ant in self.ants:
            x, y, _ = ant.coords
            for i in range(3):
                view[x, y, i] = 255
        
        # Show colony
        for i in range(3):
            x, y = self.origin
            view[x, y, i] = 166
        
        view = numpy.repeat(view, pixel_size, axis=0)
        view = numpy.repeat(view, pixel_size, axis=1)
        return view.astype('uint8')

    def spawn_ant(self, amount=1):
        """Add a new ant to the colony"""
        for _ in range(amount):
            x, y = self.origin
            self.ants.append(
                Ant((x, y, 'HUNGRY'), self.MAX_SCENT_INTENSITY)
            )
    
    def spawn_food(self, 
        pixel : Optional[Tuple[int, int]] = None,
        rectangle : Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None,
        circle: Optional[Tuple[int, int, int]] = None
        ):
        """Spawn food in the area"""
        if pixel is not None:
            self.food.add(pixel)

        if rectangle is not None:
            min_x = min(max(0, min(rectangle[0][0], rectangle[1][0])), self.size[0]-1)
            max_x = min(max(0, max(rectangle[0][0], rectangle[1][0])), self.size[0]-1)
            min_y = min(max(0, min(rectangle[0][1], rectangle[1][1])), self.size[1]-1)
            max_y = min(max(0, max(rectangle[0][1], rectangle[1][1])), self.size[1]-1)

            for x in range(min_x, max_x+1):
                for y in range(min_y, max_y+1):
                    self.food.add((x, y))
        
        if circle is not None:
            cx, cy, r = circle
            min_x = max(0, min(cx-r, self.size[0]-1))
            max_x = max(0, min(cx+r, self.size[0]-1))
            min_y = max(0, min(cy-r, self.size[1]-1))
            max_y = max(0, min(cy+r, self.size[1]-1))

            for x in range(min_x, max_x+1):
                for y in range(min_y, max_y+1):
                    euclid_dist = abs(cx-x)**2 + abs(cy-y)**2
                    if euclid_dist <= r**2:
                        self.food.add((x, y))
        

    def __decay_scent(self):
        """Remove scent when it's around for too long"""
        s = self.scent
        for x in s:
            sx = s[x]
            for y in sx:
                sy = sx[y]
                for z in sy:
                    sy[z] += -1

                sx[y] = {z:sy[z] for z in sy if sy[z] > 0}
            s[x] = {y:sx[y] for y in sx if sx[y] != {}}
        self.scent = {x:s[x] for x in s if s[x] != {}}