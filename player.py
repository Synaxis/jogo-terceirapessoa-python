import math

from entity import Entity
from settings import PLAYER, PLAYER_SIZE, PLAYER_SPEED


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SIZE, PLAYER)
        self.angle = 0.0

    def update(self, keys, walls, world_w, world_h):
        dx = (1 if keys["d"] else 0) - (1 if keys["a"] else 0)
        dy = (1 if keys["s"] else 0) - (1 if keys["w"] else 0)

        if dx or dy:
            length = math.hypot(dx, dy)
            dx = dx / length * PLAYER_SPEED
            dy = dy / length * PLAYER_SPEED
            self.angle = math.atan2(dy, dx)
            self.move(dx, dy, walls)
            self.clamp(world_w, world_h)
