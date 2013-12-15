import random

random.seed("Squeamish Ossifrage")

def r():
    return random.random() * random.random()

class EntityEventTypes:

    MOVEMENT = r()
    PLAYER_EVENT = r()

class WorldEventTypes:
    ENTITY_MOVEMENT = r()

class DamageType:
    pass


class Event(object):
    def __init__(self, name, sender, type_=None, movement=None, packaged_event=None, **kwargs):
        self.name = name
        self.sender = sender
        self.reciever = None

        if type_ == EntityEventTypes.PLAYER_EVENT:
            self.type = EntityEventTypes.PLAYER_EVENT
            self.packaged_event = packaged_event
        elif type_ == WorldEventTypes.ENTITY_MOVEMENT:
            self.type = WorldEventTypes.ENTITY_MOVEMENT
            self.old_position = kwargs["old_position"]
        elif movement is not None:
            self.x, self.y = movement
            self.type = EntityEventTypes.MOVEMENT