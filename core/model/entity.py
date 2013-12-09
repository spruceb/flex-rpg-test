import events


class Entity(object):
    """The entity class is the super for any part of a world that is not terrain

    Terrain being a tile-based integer indexed landscape, so "not-terrain" basically means "position is a float".
    """

    def __init__(self, position, world, health):
        self.x, self.y = position
        self.world = world
        self.health = health


    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value

    def move(self, x=0, y=0):
        self.x += x
        self.y += y

    def send(self, event):
        if event.type == events.EventTypes.MOVEMENT:
            self.move(event.x, event.y)

    def update(self):
        pass