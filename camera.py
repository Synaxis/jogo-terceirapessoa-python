class Camera:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.x = 0.0
        self.y = 0.0

    def update(self, target, world_w, world_h, smooth):
        target_x = target.x - self.w / 2
        target_y = target.y - self.h / 2 + 90

        self.x += (target_x - self.x) * smooth
        self.y += (target_y - self.y) * smooth

        self.x = max(0, min(world_w - self.w, self.x))
        self.y = max(0, min(world_h - self.h, self.y))
