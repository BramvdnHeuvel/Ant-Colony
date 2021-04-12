# viewer.py
# (c) 2020 Karthik Karanth, MIT License

from typing import Tuple, Callable, Optional
import pygame

class Viewer:
    def __init__(self, display_size : Tuple[int, int], 
        update_func : Callable, 
        pixel_size : Optional[int] = 1, 
        on_mouse_down : Optional[Callable] = None, 
        frames_per_sec : Optional[int] = None):
        """Create a Viewer object that updates the pygame UI"""

        # Obligatory values
        self.update_func = update_func

        # Optional values
        self.on_mouse_down = on_mouse_down
        self.pixel_size = pixel_size
        self.fps = frames_per_sec
        
        pygame.init()

        w, h = display_size
        self.display = pygame.display.set_mode(
            (w*self.pixel_size, h*self.pixel_size)
        )
    
    def set_title(self, title):
        pygame.display.set_caption(title)
    
    def start(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            if self.fps:
                clock.tick(self.fps)

            for event in pygame.event.get():
                # Stop game when clicked away
                if event.type == pygame.QUIT:
                    running = False
            
            # Do something whenever the user has their mouse pressed
            if self.on_mouse_down is not None and pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                self.on_mouse_down(x//self.pixel_size, y//self.pixel_size)

            Z = self.update_func()
            surf = pygame.surfarray.make_surface(Z)
            self.display.blit(surf, (0, 0))

            pygame.display.update()

        pygame.quit()