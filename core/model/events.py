import random
from ..utils import Vector

random.seed("Squeamish Ossifrage")

def r(n):
    while True:
        yield n
        n += 1
i = r(0)
def id():
    return next(i)
class EntityEventTypes:
    MOVEMENT = id()
    VELOCITY = id()
    NORMALIZED_VELOCITY = id()
    ACCELERATION = id()
    PLAYER_EVENT = id()

class WorldEventTypes:
    ENTITY_MOVEMENT = id()

class DamageType:
    pass


class Event(object):
    def __init__(self, name, sender, receiver=None, type_=None, movement=None, packaged_event=None, **kwargs):
        self.name = name
        self.sender = sender
        self.receiver = receiver
        self.type = type_
        self.constructors = {EntityEventTypes.PLAYER_EVENT: self.player_event,
                             EntityEventTypes.MOVEMENT: self.entity_movement,
                             EntityEventTypes.VELOCITY: self.entity_movement,
                             EntityEventTypes.NORMALIZED_VELOCITY: self.normalized_velocity,
                             WorldEventTypes.ENTITY_MOVEMENT: self.world_entity_movement}
        self.constructors[self.type](kwargs)


    def player_event(self, kwargs):
        self.packaged_event = kwargs["packaged_event"]

    def world_entity_movement(self, kwargs):
        self.old_position = kwargs["old_position"]

    def entity_movement(self, kwargs):
        self.movement = kwargs["movement"]
        self.x, self.y = self.movement

    def normalized_velocity(self, kwargs):
        speed = kwargs["speed"]
        direction = kwargs["direction"].norm
        self.velocity = direction * speed