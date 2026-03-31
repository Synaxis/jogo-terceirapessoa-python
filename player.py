from entity import Entity
from settings import PLAYER_SIZE


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SIZE, "#57d3ff")

    def update(self, keys, walls, world_w, world_h):
        dx = (1 if keys["d"] else 0) - (1 if keys["a"] else 0)
        dy = (1 if keys["s"] else 0) - (1 if keys["w"] else 0)

        if dx or dy:
            if dx and dy:
                dx *= 0.7071
                dy *= 0.7071
            self.move(dx * 5.6, dy * 5.6, walls)
            self.clamp(world_w, world_h)
