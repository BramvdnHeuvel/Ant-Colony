from typing import Dict, Tuple
from itertools import product
import random

class Ant:
    def __init__(self,  
            coords : Tuple[int, int, int],
            intensity : int
            ):
        self.intensity = intensity
        self.direction = (0, 0)
        self.coords = coords
    
    @property
    def state(self):
        return self.coords[2]

    def move(self, 
        scent : Dict[int, Dict[int, Dict[int, int]]],
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

        if x not in s:
            s[x] = {y: {z: self.intensity}}
        elif y not in s[x]:
            s[x][y] = {z: self.intensity}
        else:
            s[x][y][z] = self.intensity

    
    def __choose_direction(self, 
            border: Tuple[int, int],
            colony_scent : Dict[int, Dict[int, Dict[int, int]]]
                ) -> Tuple[int, int]:
        """Choose a direction to head towards"""
        x, y, z = self.coords
        pfx, pfy = self.direction

        # Determine how attractive nearby tiles are
        attractive = {}
        neutral = []
        unattractive = {}
        for dx, dy in product([-1, 0, 1], repeat=2):
            if dx == dy:
                continue
            if abs(pfx-dx) + abs(pfy-dy) == 4:
                continue
            if pfx == dx == 0 and pfy != dy:
                continue
            if pfy == dy == 0 and pfx != dx:
                continue
            if x+dx < 0 or border[0] <= x+dx:
                continue
            if y+dy < 0 or border[1] <= y+dy:
                continue

            try:
                flavours = colony_scent[x+dx][y+dy]
            except KeyError:
                flavours = {}

            for f in flavours:
                if f != z:
                    attractive[dx, dy] = flavours[f]
                    break
            else:
                if z in flavours:
                    unattractive[dx, dy] = flavours[z]
                #else:
                neutral.append((dx, dy))

        # How attractive is our own tile?
        try:
            flavours = colony_scent[x][y]
        except KeyError:
            current_attraction = False
        else:
            for f in flavours:
                if f != z:
                    current_attraction = True
                    break
            else:
                current_attraction = False

        if attractive != {} and random.random() < 0.75:
            # We're picky if we're already in a good spot
            if current_attraction:
                least_scent = min(attractive.values())
                options = [key for key in attractive if attractive[key] == least_scent]
                return random.choice(options)
            # Otherwise, take the most smelly place
            else:
                least_scent = max(attractive.values())
                options = [key for key in attractive if attractive[key] == least_scent]
                return random.choice(options)

        elif neutral != []:
            return random.choice(neutral)

        elif unattractive != {}:
            if random.random() < 0.25:
                return random.choice([k for k in unattractive])
            else:
                least_scent = max(unattractive.values())
                options = [key for key in unattractive if unattractive[key] == least_scent]
                return random.choice(options)

        else:
            # Ant cornered itself, or got confused
            return -1*pfx, -1*pfy

