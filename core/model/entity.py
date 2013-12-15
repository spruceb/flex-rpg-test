import events


class Entity(object):
    """The entity class is the super for any part of a world that is not terrain

    Terrain being a tile-based integer indexed landscape, so "not-terrain" basically means "position is a float".
    """

    def __init__(self, position, world, health, type):
        self.x, self.y = position
        self.world = world
        self.health = health
        self.goal = None
        self.velocity_x = 0
        self.velocity_y = 0
        self.type = type

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def velocity(self):
        return self.velocity_x, self.velocity_y

    @velocity.setter
    def velocity(self, value):
        self.velocity_x, self.velocity_y = value

    def move(self, time):
        old_position = self.position
        self.position = self.x + (self.velocity_x*time), self.y + (self.velocity_y*time)
        movement_event = events.Event(sender=self, type_=events.WorldEventTypes.ENTITY_MOVEMENT, old_position=old_position)
        self.world.send(movement_event)

    def send(self, event):
        if event.type == events.EntityEventTypes.MOVEMENT:
            self.velocity = event.x, event.y

    def update(self, time):
        """Time is float in seconds. All velocity values are pseudo-dimensionless (self.positions per second)
        """
        self.move(time)
