class Entity:
    def __init__(self, x, y, size, color):
        self.x = float(x)
        self.y = float(y)
        self.size = size
        self.color = color

    @property
    def left(self):
        return self.x - self.size

    @property
    def right(self):
        return self.x + self.size

    @property
    def top(self):
        return self.y - self.size

    @property
    def bottom(self):
        return self.y + self.size

    def _hits(self, wall):
        x, y, w, h = wall
        return self.right > x and self.left < x + w and self.bottom > y and self.top < y + h

    def move(self, dx, dy, walls):
        self.x += dx
        for wall in walls:
            if self._hits(wall):
                x, _, w, _ = wall
                if dx > 0:
                    self.x = x - self.size
                elif dx < 0:
                    self.x = x + w + self.size

        self.y += dy
        for wall in walls:
            if self._hits(wall):
                _, y, _, h = wall
                if dy > 0:
                    self.y = y - self.size
                elif dy < 0:
                    self.y = y + h + self.size

    def clamp(self, world_w, world_h):
        self.x = max(self.size, min(world_w - self.size, self.x))
        self.y = max(self.size, min(world_h - self.size, self.y))
