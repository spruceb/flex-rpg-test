from collections import defaultdict as dd
import functools
import entity
from events import EventTypes


class TerrainTile(object):
    def __init__(self, type_):
        self.type = type_
        self.health = 100


class World(object):
    def __init__(self, input=None):
        if input is not None:
            self.build(input)
        else:
            self.generate()
        self.terrain = dd(self.default_terrain)
        self.player = entity.Entity((0, 0), self, 100)
        self.entities = [self.player]

    def build(self, input):
        pass

    def generate(self):
        pass

    def default_terrain(self):
        return TerrainTile("grass")

    def send(self, event):
        if event.type == EventTypes.PLAYER_EVENT:
            self.player.send(event.packaged_event)
