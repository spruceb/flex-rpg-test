import random

random.seed(5)


class EventTypes:
    MOVEMENT = random.random()
    PLAYER_EVENT = random.random()


class DamageType:
    pass


class Event(object):
    def __init__(self, name, sender, type_=None, movement=None, packaged_event=None):
        self.name = name
        self.sender = sender
        self.reciever = None

        if type_ == EventTypes.PLAYER_EVENT:
            self.type = EventTypes.PLAYER_EVENT
            self.packaged_event = packaged_event
        elif movement is not None:
            self.x, self.y = movement
            self.type = EventTypes.MOVEMENT