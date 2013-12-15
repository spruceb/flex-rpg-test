import pygame
from pygame_colors import *
from pygame import locals
from itertools import product
import sys


class Display(object):
    TILE_SIZE = 32

    def __init__(self, display_size=(0, 0), display_modes=(0, 32)):
        pygame.init()
        self.display_surface = pygame.display.set_mode(display_size, *display_modes)
        self.display_surface.fill(WHITE)

    def float_to_pix(self, position):
        pass

    def update(self, terrain, focus_pos, focus_sprite, ):
        # Rewrite

        self.display_surface.fill(BLACK)
        start_pix = tuple(-int((n - int(n)) * self.TILE_SIZE) for n in focus_pos)
        ends = tuple(int(n / self.TILE_SIZE) + 1 for n in self.display_surface.get_size())
        terrain_range_x, terrain_range_y = tuple(range(int(p)-1, e+int(p)) for p, e in zip(focus_pos, ends))

        for i_x, x in enumerate(terrain_range_x):
            for i_y, y in enumerate(terrain_range_y):
                tile = terrain.get((x, y))
                curr_pix_pos = tuple(n + (i-1) * self.TILE_SIZE for n, i in zip(start_pix, (i_x, i_y)))

                if tile is not None:
                    self.display_surface.blit(tile, curr_pix_pos)
                else:
                    print tile

        self.display_surface.blit(focus_sprite, map(lambda x,y: x-(y/2), self.display_surface.get_rect().center, focus_sprite.get_rect().center))

        pygame.display.update()

    def update(self, terrain, focus_pos, entities):
        pass
    @property
    def pygame_events(self):
        return pygame.event.get()