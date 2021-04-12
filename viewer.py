# viewer.py
# (c) 2020 Karthik Karanth, MIT License

import pygame

class Viewer:
    def __init__(self, update_func, display_size, pixel_size, on_mouse_down=None, frames_per_sec=None):
        self.fps = frames_per_sec
        self.update_func = update_func
        self.on_mouse_down = on_mouse_down
        self.pixel_size = pixel_size
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
                if event.type == pygame.QUIT:
                    running = False
            
            if self.on_mouse_down is not None and pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                self.on_mouse_down(x//self.pixel_size, y//self.pixel_size)

            Z = self.update_func()
            surf = pygame.surfarray.make_surface(Z)
            self.display.blit(surf, (0, 0))

            pygame.display.update()

        pygame.quit()