from entity import Entity


class Npc(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 24, "#ff8a57")

    def update(self, player, walls, world_w, world_h):
        dx = 1 if player.x > self.x else -1
        dy = 1 if player.y > self.y else -1
        self.move(dx * 1.3, dy * 1.3, walls)
        self.clamp(world_w, world_h)
