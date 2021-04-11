from typing import Dict, Tuple
from itertools import product
import random

class Ant:
    def __init__(self,  
            coords : Tuple[int, int, int]
            ):
        self.direction = (0, 0)
        self.coords = coords
    
    @property
    def state(self):
        return self.coords[2]

    def move(self, 
        scent : Dict[int, Dict[int, Dict[int, int]]],
        border : Tuple[int, int], intensity : int
            ) -> Tuple[int, int]:
        """Move on the board"""
        dx, dy = self.__choose_direction(border, scent)
        self.leave_scent(scent, intensity)
        
        x, y, z = self.coords
        self.coords = (x+dx, y+dy, z)
        self.direction = (dx, dy)
        return x+dx, y+dy
        
    def change_state(self, state : int) -> None:
        """Change the ant's state, effectively
           altering their walking behaviour."""
        x, y, _ = self.coords
        self.coords = (x, y, state)

    def leave_scent(self, s, intensity : int):
        """Leave behind a scent to pick up"""
        x, y, z = self.coords

        if x not in s:
            s[x] = {y: {z: intensity}}
        elif y not in s[x]:
            s[x][y] = {z: intensity}
        else:
            s[x][y][z] = intensity

    
    def __choose_direction(self, 
            border: Tuple[int, int],
            colony_scent : Dict[int, Dict[int, Dict[int, int]]]
                ) -> Tuple[int, int]:
        """Choose a direction to head towards"""
        x, y, z = self.coords
        pfx, pfy = self.direction

        scents = {(a, b): 0 for a, b in product([-1, 0, 1], repeat=2) if not (a==b==0)}

        # Directions that the ant could walk to
        for dx, dy in scents:
            preferred_direction = 4 - abs(pfx-dx) - abs(pfy-dy)
            preferred_direction += -2*int(pfx==dx==0 or pfy==dy==0)
            scents[dx, dy] += preferred_direction

            # Directions from which it smells the scent
            for scx, scy in scents:

                try:
                    flavours = colony_scent[x+dx][y+dy]
                except KeyError:
                    flavours = {}
                linear_dependence = 4 - abs(dx-scx) - abs(dy-scy)
                linear_dependence += -2*int(scx==dx==0 or scy==dy==0)

                # Determine whether scents work
                # positively or negatively
                attraction = 0

                for f in flavours:
                    if f == z:
                        # Same scent disperses
                        pass
                        #attraction += flavours[f] * (4-linear_dependence) * preferred_direction
                    else:
                        # Other scents attract
                        attraction += flavours[f] * linear_dependence * preferred_direction

                scents[dx, dy] += attraction

        # Remove all directions that are out of boundaries
        scents = {
            (dx, dy): scents[dx, dy] for dx, dy in scents
            if 0 <= x+dx < border[0] and 0 <= y+dy < border[1]
        }

        # Once the attraction of all
        # directions is determined,
        # we randomly pick one.
        choice = random.random() * sum(scents.values())
        current = 0
        for dx, dy in scents:
            current += scents[dx, dy]
            if current >= choice:
                return dx, dy
        else:
            raise ValueError(
                "Impossible random value detected - maybe an ant was forced to walk backwards?"
            )