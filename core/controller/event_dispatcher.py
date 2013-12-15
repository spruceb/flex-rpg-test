from ..model import events, world, entities
from ..view import display
from collections import defaultdict as dd
import pygame
from pygame import locals
import sys
import os
import time

SPEED = 6

class Dispatcher(object):
    def __init__(self, world_input=None):
        self.world = world.World(world_input)
        self.display = display.Display()
        self.sprites = {"grasstile.png": pygame.image.load(os.path.realpath("./../rogue/core/resources/terrain/grasstile.png")),
                        "test_egg.png": pygame.image.load(os.path.realpath("./../rogue/core/resources/entities/test_egg.png")),
                        "red.png": pygame.image.load(os.path.realpath("./../rogue/core/resources/entities/red.png"))}
        self.player = self.world.player
        self.last_update = None

    def sprite(self, model_item):
        if hasattr(model_item, "position"):
            return self.entity_sprite(model_item)
        else:
            return self.terrain_sprite(model_item)
    
    def terrain_sprite(self, terrain_item):
        return self.sprites["grasstile.png"]
    def entity_sprite(self, entity_item):
        if entity_item.type == 'player':
            return self.sprites["test_egg.png"]
        elif entity_item.type == 'fireball':
            return self.sprites['red.png']
    def wrapped_terrain(self, terrain):
        def _():
            pass

        def get(key):
            return self.terrain_sprite(terrain[key])
        _.get = get

        return _
    def set_entity_velocity(self, entity, x=None, y=None):
        if x is None: x = entity.velocity_x
        if y is None: y = entity.velocity_y
        move = events.Event('dipatcher_velocity_set', events.EntityEventTypes.MOVEMENT, movement=(x,y))
        entity.send(move)

    def update(self):
        if self.last_update is None:
            self.last_update = time.time()

        self.display.update(self.wrapped_terrain(self.world.terrain), self.player.position, self.sprite(self.player))

        for event in self.display.pygame_events:
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_a:
                    self.set_entity_velocity(self.player, x=-SPEED)
                elif event.key == locals.K_d:
                    self.set_entity_velocity(self.player, x=SPEED)
                elif event.key == locals.K_w:
                    self.set_entity_velocity(self.player, y=-SPEED)
                elif event.key == locals.K_s:
                    self.set_entity_velocity(self.player, y=SPEED)

                if event.key == locals.K_SPACE:
                    fireball = entities.Entity(self.player.position, self.world, 1, 'fireball')
                    self.set_entity_velocity(fireball, *(6*bool(v) for v in self.player.velocity))
                    print fireball.velocity
                    self.world.entities.append(fireball)
            if event.type == locals.KEYUP:
                if event.key in (locals.K_w,locals.K_s):
                    self.set_entity_velocity(self.player, y=0)
                elif event.key in (locals.K_d, locals.K_a):
                    self.set_entity_velocity(self.player, y=0)

        for e in self.world.entities:
            e.update(time.time() - self.last_update)

        self.last_update = time.time()
