import events
from events import EntityEventTypes, WorldEventTypes
from ..utils import Vector
from decimal import Decimal as dec
import time

Point = Vector

class Entity(object):
    """
    The entity class is the super for any part of a world that is not terrain

    Terrain being a tile-based integer indexed landscape, so "not-terrain" basically means "position is a float".
    """

    APPROACH_DT_MULTIPLIER = 10**2

    def __init__(self, position, world, health, type):
        self.x, self.y = position
        self.world = world
        self.health = health
        self.position = Point(position)
        self.velocity = Vector(0, 0)
        self.velocity_goal = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.type = type
        self.face_vector = Vector(1, 0)
        self.last_update = time.time()

    def approach(self, dt):
        dt *= self.APPROACH_DT_MULTIPLIER
        def approach_scalar(v, g):
            if g - v > dt:
                return (v + dt)
            elif g - v > -dt:
                return (v - dt)
            return g
        return Vector(map(approach_scalar, self.velocity, self.velocity_goal))

    def move(self, dt):
        """Updates position based on velocity and dt, and velocity based on acceleration. Informs world of movement."""
        old_position = self.position
        self.position += (self.velocity * dt)
        #self.velocity = self.approach(dt)
        self.velocity += (self.acceleration * dt)
        movement_event = events.Event(name="entity_move", sender=self, type_=events.WorldEventTypes.ENTITY_MOVEMENT, old_position=old_position)
        self.world.send(movement_event)

    def send(self, event):
        if event.type == EntityEventTypes.NORMALIZED_VELOCITY:
            self.velocity = event.velocity

    def update(self):
        """
        dt (delta time) is float of seconds. All velocity values are pseudo-dimensionless (self.positions per second)
        """
        dt = time.time() - self.last_update
        self.move(dt)
        self.last_update = time.time()