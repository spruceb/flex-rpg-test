from ..model import events, world, entities
from ..view import display
from ..model.events import EntityEventTypes, WorldEventTypes
from operator import sub, mul, add, truediv
from collections import defaultdict as dd
import pygame
from pygame import locals
import sys
import os
import time
from ..utils import Vector

class Directions:
    NORTH = Vector(0, 1)
    EAST = Vector(1, 0)
    SOUTH = Vector(0, -1)
    WEST = Vector(-1, 0)



SPEED = 3
# TODO: Figure out a way to display entities with large sprites that are centered offscreen
# TODO: Figure out collision (probably using pygame masks + sprites)

class Dispatcher(object):
    def __init__(self, world_input=None):
        self.world = world.World(world_input)
        self.display = display.Display()

        # Temporary dictionary of sprites
        self.sprites = {"grasstile.png": pygame.image.load(os.path.realpath("./../rogue/core/resources/terrain/stone.png")).convert_alpha(),
                        "test_egg.png": pygame.image.load(os.path.realpath("./../rogue/core/resources/entities/test_egg.png")).convert_alpha(),
                        "red.png": pygame.image.load(os.path.realpath("./../rogue/core/resources/entities/red.png")).convert_alpha()}
        self.player = self.world.player
        self.last_update = None
        self.x_set = self.y_set = 0

    def sprite(self, model_item):
        '''Returns the sprite of a given entity (entity sprites are attached to the entity itself, but rather the view it is part of)'''
        if isinstance(model_item, entities.Entity):
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

    @property
    def wrapped_terrain(self):
        '''Insane, stupid way of getting the sprites for terrain tiles'''
        class _:
            pass

        def get(key):
            return self.terrain_sprite(self.world.terrain[key])
        _.get = get

        return _

    def set_entity_velocity(self, entity, x=None, y=None):
        move = events.Event('dipatcher_velocity_set', self, type_=EntityEventTypes.VELOCITY, movement=(x,y), receiver=entity)
        entity.send(move)

    def set_normalized_velocity(self, entity, speed, direction):
        norm_v = events.Event(name="norm_velocity", sender=self, type_=EntityEventTypes.NORMALIZED_VELOCITY, speed=speed, direction=Vector(direction))
        entity.send(norm_v)

    def keypress_handler(self, key_event):

        if key_event.type == locals.KEYDOWN:

            if key_event.key == locals.K_a:
                self.x_set = -1
            elif key_event.key == locals.K_d:
                self.x_set = 1
            elif key_event.key == locals.K_w:
                self.y_set = -1
            elif key_event.key == locals.K_s:
                self.y_set = 1

            if key_event.key == locals.K_SPACE:
                fireball = entities.Entity(self.player.position, self.world, 1, 'fireball')
                self.set_normalized_velocity(fireball, 2.9, Vector(bool(v) for v in self.player.velocity))
                self.world.add_entity(fireball)

            if key_event.key == locals.K_q:
                pygame.event.post(pygame.event.Event(locals.QUIT))
        if key_event.type == locals.KEYUP:
            if key_event.key in (locals.K_w,locals.K_s):
                self.y_set = 0
            elif key_event.key in (locals.K_d, locals.K_a):
                self.x_set = 0
        self.set_normalized_velocity(self.player, SPEED, (self.x_set, self.y_set))

    def world_update(self):
        for e in self.world.entity_list:
            e.update()

    def display_update(self, focus):
        for event in self.display.pygame_events:
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (locals.KEYDOWN, locals.KEYUP):
                self.keypress_handler(event)

        def pos_to_pix(pos):
            return map(lambda x, y, z: int(x + (z-y)*self.display.tile_size), self.display.size.center, focus, pos)

        tiles_from_edge = [truediv(n, self.display.tile_size)+1 for n in self.display.size.center]
        display_start = map(int, map(sub, focus, tiles_from_edge))
        display_end = map(int, map(add, focus, tiles_from_edge))
        print "display", display_start, display_end, focus
        displayed_entities = list(self.world.entity_container.get_box(display_start, map(sub, display_end, display_start)))
        print "entities", list(displayed_entities)
        wrapped_entities = ((self.sprite(e), pos_to_pix(e.position)) for e in displayed_entities)

        self.display.update(self.wrapped_terrain, wrapped_entities, pos_to_pix, display_start, display_end)


    def update(self):
        if self.last_update is None:
            self.last_update = time.time()
        #dt = time.time() - self.last_update
        self.world_update()
        self.display_update(self.player.position)

        self.last_update = time.time()
