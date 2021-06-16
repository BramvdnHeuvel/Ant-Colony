from typing import Dict, Tuple
from itertools import product
import random

class Ant:
    def __init__(self,  
                coords : Tuple[int, int, int],
                intensity : int,
                max_intensity : int
                ):
        self.intensity = intensity
        self.max_intensity = max_intensity
        self.direction = (0, 0)
        self.coords = coords
    
    @property
    def state(self):
        return self.coords[2]

    def move(self, 
        scent : Dict[int, Dict[int, Dict[int, Tuple[int, int, int]]]],
        border : Tuple[int, int]) -> Tuple[int, int]:
        """Move on the board"""
        dx, dy = self.__choose_direction(border, scent)
        self.leave_scent(scent)
        
        x, y, z = self.coords
        self.coords = (x+dx, y+dy, z)
        self.direction = (dx, dy)
        return x+dx, y+dy
        
    def change_state(self, state : int) -> None:
        """Change the ant's state, effectively
           altering their walking behaviour."""
        x, y, _ = self.coords
        self.coords = (x, y, state)

    def leave_scent(self, s):
        """Leave behind a scent to pick up"""
        x, y, z = self.coords
        dx, dy = self.direction
        scent = (-1*dx, -1*dy, self.intensity)

        if x not in s:
            s[x] = {y: {z: scent}}
        elif y not in s[x]:
            s[x][y] = {z: scent}
        elif z not in s[x][y]:
            s[x][y][z] = scent
        else:
            # If the scent already exists,
            # don't alter the direction
            # but make it stronger
            pass
        
        # Refurbish all existing scents
        for f in s[x][y]:
            dx, dy, i = s[x][y][f]
            if f == z:
                s[x][y][f] = (dx, dy,
                    min(i + self.intensity, self.max_intensity))
            else:
                s[x][y][f] = (dx, dy,
                    min(int(i*1.5), self.max_intensity))
    
    def __choose_direction(self, 
            border: Tuple[int, int],
            colony_scent : Dict[int, Dict[int, Dict[int, int]]]
                ) -> Tuple[int, int]:
        """Choose a direction to head towards"""
        x, y, z = self.coords
        dx, dy = 0, 0
        try:
            current = colony_scent[x][y]
        except KeyError:
            # Check whether a nearby spot
            # has a scent
            possible = []
            for dx, dy in product([-1, 0, 1], repeat=2):
                if dx==dy==0:
                    continue
                try:
                    s = colony_scent[x+dx][y+dy]
                except KeyError:
                    pass
                else:
                    for f in s:
                        if f != z:
                            possible.append((dx, dy))
                            break
            if len(possible) > 0:
                dx, dy = random.choice(possible)
            else:
                dx, dy = 0, 0
        else:
            # The scent has a direction! Therefore,
            # take that direction.
            for f in current:
                if f != z:
                    dx, dy = current[f][0], current[f][1]
            else:
                if z in current:
                    possible = []
                    for dx, dy in product([-1, 0, 1], repeat=2):
                        if dx == dy == 0:
                            continue

                        try:
                            colony_scent[x+dx][y+dy][z]
                        except KeyError:
                            possible.append((dx, dy))
                    
                    dx, dy = 0, 0
                    if len(possible) > 0:
                        dx, dy = random.choice(possible)


        # No scent is found, so take a random path
        while ((abs(dx) + abs(dy) == 0) or
              (x+dx < 0 or x+dx >= border[0]) or
              (y+dy < 0 or y+dy >= border[1]) or
              (dx==self.direction*-1 and dy==self.direction*-1)):
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
        return dx, dy
