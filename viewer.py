# viewer.py
# (c) 2020 Karthik Karanth, MIT License

import pygame

class Viewer:
    def __init__(self, update_func, display_size, frames_per_sec=None):
        self.fps = frames_per_sec
        self.update_func = update_func
        pygame.init()
        self.display = pygame.display.set_mode(display_size)
    
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

            Z = self.update_func()
            surf = pygame.surfarray.make_surface(Z)
            self.display.blit(surf, (0, 0))

            pygame.display.update()

        pygame.quit()