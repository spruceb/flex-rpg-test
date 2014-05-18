from collections import defaultdict
import itertools as it
import entities
import events
from events import EntityEventTypes, WorldEventTypes


class TerrainTile(object):
    def __init__(self, type_):
        self.type = type_
        self.health = 100

class EntityContainer:
    """
    Contains entities ordered by what tile they're in.

    Has a private dictionary with integer keys. Each key represents a row of tiles and is paired with another integer
    dictionary (of "tiles"). Each of the values is a list of the entities within that tile. Does not contain any
    empty rows/nodes. Whenever an entity moves from its tile it must be deleted and re-added to its EntityContainer
    to keep the structure intact. This is the job of the World/EventDispatcher that owns the entity.
    """

    def __init__(self, elements):
        self._elements = {}
        self.extend(elements)

    def __getitem__(self, key):
        """
        Return the list of entities at the tile specified by key, an (x, y) tuple.
        Return an empty list if there none.
        """
        return (self._elements.get(key[1]) or {}).get(key[0], [])

    def get_box(self, start_coords, size):
        """
        Return all entities contained within the rectangle specified by `start_coords` and `size`

        `start_coords` is the (x, y) coordinate of the top left corner of the rectangle. `size` is the (height, width)
        of the rectangle. The returned list is flat and has no defined order.
        """
        start_x, start_y = start_coords
        width, height = size
        print "box", start_coords, size
        indices = it.product(xrange(start_x, start_x + width), xrange(start_y, start_y + height))
        return it.chain(*it.imap(self.__getitem__, indices))

    def add(self, entity):
        """Adds an entity to the container"""
        x, y = map(int, entity.position)
        row = self._elements.get(y, None)
        if row is None:
            self._elements[y] = row = {}
        tile = row.get(x, None)
        if tile is None:
            self._elements[y][x] = tile = []
        if entity not in tile: tile.append(entity)
        return self

    def extend(self, entities_):
        for entity in entities_:
            self.add(entity)
        return self

    def delete(self, entity, tile_coords=None):
        """
        Removes an entity from the collection.

        If the entity was the last in its tile, removes the tile (and ditto with row).
        Raises: KeyError if an invalid `entity` is provided, and ValueError if the entity doesn't exist in its
        supposed tile.
        """
        x, y = map(int, entity.position) if tile_coords is None else map(int, tile_coords)
        tile = self[x,y]
        tile.remove(entity)
        if not tile:
            self._elements[y].pop(x)
            if not self._elements[y]:
                self._elements.pop(y)
        return self

    def update(self, old_position, entity):
        """Given an entity's previous position, updates its place in the data structure after movement"""
        position = map(int, entity.position)
        if position != old_position:
            self.delete(entity, old_position).add(entity)
        return self

    def all(self):
        return sum((tile for row in self._elements.itervalues() for tile in row.itervalues()), [])

class World(object):
    def __init__(self, input=None):
        if input is not None:
            self.build(input)
        else:
            self.generate()
        self.terrain = defaultdict(self.default_terrain)
        self.player = entities.Entity((0, 0), self, 100, "player")
        self.entity_list = [self.player]
        self.entity_container = EntityContainer(self.entity_list)

    def build(self, input):
        pass

    def generate(self):
        pass

    def add_entity(self, entity):
        self.entity_list.append(entity)
        self.entity_container.add(entity)
        return self

    def remove_entity(self, entity):
        self.entity_list.append(entity)
        self.entity_container.delete(entity)
        return self

    def default_terrain(self):
        return TerrainTile("grass")

    def send(self, event):
        if event.type == EntityEventTypes.PLAYER_EVENT:
            self.player.send(event.packaged_event)
        elif event.type == WorldEventTypes.ENTITY_MOVEMENT:
            self.entity_container.update(event.old_position, event.sender)