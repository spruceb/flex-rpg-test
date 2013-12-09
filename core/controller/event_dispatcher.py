from ..model import events, world, entity
from ..view import display
from collections import defaultdict as dd
import pygame
from pygame import locals as pyg_consts
import sys



class Dispatcher(object):
    def __init__(self, world_input=None):
        self.world = world.World(world_input)
        self.display = display.Display()
        self.sprites = {"grasstile.png": pygame.image.load("/Users/Spruce/Organization/Developer/Languages/Python/Workspace/rogue/core/resources/terrain/grasstile.png")}

    def sprite(self, model_item):
        if hasattr(model_item, "position"):
            return self.entity_sprite(model_item)
        else:
            return self.terrain_sprite(model_item)
    
    def terrain_sprite(self, terrain_item):
        return self.sprites["grasstile.png"]
    def wrapped_terrain(self, terrain):
        def _():
            pass
        def get(key):
            return self.terrain_sprite(terrain[key])
        _.get = get

        return _

    def update(self):
        self.display.update(self.wrapped_terrain(self.world.terrain), self.world.player.position)
        for event in self.display.pygame_events:
            if event.type == pyg_consts.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pyg_consts.KEYDOWN and event.key == pyg_consts.K_LEFT:
                self.world.player.x