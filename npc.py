import math

from entity import Entity
from settings import NPC, NPC_SIZE, NPC_SPEED


class Npc(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, NPC_SIZE, NPC)
        self.angle = 0.0

    def update(self, player, walls, world_w, world_h):
        vx = player.x - self.x
        vy = player.y - self.y
        dist = math.hypot(vx, vy)
        if dist < 1:
            return

        speed = NPC_SPEED if dist < 420 else NPC_SPEED * 0.35
        dx = vx / dist * speed
        dy = vy / dist * speed
        self.angle = math.atan2(dy, dx)
        self.move(dx, dy, walls)
        self.clamp(world_w, world_h)
