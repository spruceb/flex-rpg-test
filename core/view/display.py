import pygame
from pygame_colors import *
import os
from operator import sub
from pygame import locals
import itertools
import sys


class Display(object):
    def __init__(self, display_size=(0, 0), display_modes=(0, 32), tile_size=32):
        pygame.init()
        self.tile_size = tile_size
        self.display_surface = pygame.display.set_mode(display_size, *display_modes)
        self.display_surface.fill(WHITE)

    @property
    def size(self):
        return self.display_surface.get_rect()


    def draw_terrain(self, terrain, focus_pos):
        start_pix = tuple(-int((n - int(n)) * self.tile_size) for n in focus_pos)
        # for x from whatever fits from focus pos

    def update(self, terrain, entities, pix_to_pos, terrain_start, terrain_end):
        self.display_surface.fill(WHITE)
        print("w00t")

        #for y in xrange(terrain_start[1], terrain_end[1]):
        #    for x in xrange(terrain_start[0], terrain_end[0]):
        #        tile = terrain.get((x, y))
        #        if tile is not None:
        #            self.display_surface.blit(tile, pix_to_pos((x, y)))

        for sprite, position in entities:
            print sprite, position, "blitted someting"
            self.display_surface.blit(sprite, position)
        pygame.display.update()

    @property
    def pygame_events(self):
        return pygame.event.get()