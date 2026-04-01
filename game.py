import math
import tkinter as tk
from config import *

def hit(x, y, r, wall):
    wx, wy, ww, wh = wall
    nx = max(wx, min(x, wx + ww))
    ny = max(wy, min(y, wy + wh))
    return (x - nx) ** 2 + (y - ny) ** 2 < r * r

def move(obj, dx, dy):
    x, y, r = obj["x"] + dx, obj["y"], obj["r"]
    if r <= x <= WORLD_W - r and not any(hit(x, y, r, w) for w in WALLS):
        obj["x"] = x

    x, y = obj["x"], obj["y"] + dy
    if r <= y <= WORLD_H - r and not any(hit(x, y, r, w) for w in WALLS):
        obj["y"] = y

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.resizable(False, False)

        self.cv = tk.Canvas(self.root, width=W, height=H, bg=BG, highlightthickness=0)
        self.cv.pack()

        self.keys = {k: 0 for k in "wasd"}
        self.root.bind("<KeyPress>", lambda e: self._set(e, 1))
        self.root.bind("<KeyRelease>", lambda e: self._set(e, 0))
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("r", self.reset)

        self.reset()
        self.tick()

    def _set(self, event, value):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = value

    def reset(self, _=None):
        self.p = {"x": 120, "y": 120, "r": PLAYER_R, "a": 0.0, "c": PLAYER}
        self.enemies = [
            {"x": 760, "y": 380, "r": ENEMY_R, "a": 0.0, "c": ENEMY},
            {"x": 1410, "y": 540, "r": ENEMY_R, "a": 0.0, "c": ENEMY},
            {"x": 560, "y": 980, "r": ENEMY_R, "a": 0.0, "c": ENEMY},
        ]

    def cam(self):
        x = max(0, min(WORLD_W - W, self.p["x"] - W / 2))
        y = max(0, min(WORLD_H - H, self.p["y"] - H / 2 + 80))
        return x, y

    def update_player(self):
        dx = self.keys["d"] - self.keys["a"]
        dy = self.keys["s"] - self.keys["w"]
        if dx or dy:
            n = math.hypot(dx, dy)
            dx = dx / n * PLAYER_SPEED
            dy = dy / n * PLAYER_SPEED
            self.p["a"] = math.atan2(dy, dx)
            move(self.p, dx, dy)

    def update_enemy(self, enemy):
        vx = self.p["x"] - enemy["x"]
        vy = self.p["y"] - enemy["y"]
        d = math.hypot(vx, vy)
        if d > 1:
            dx = vx / d * ENEMY_SPEED
            dy = vy / d * ENEMY_SPEED
            enemy["a"] = math.atan2(dy, dx)
            move(enemy, dx, dy)

    def draw_actor(self, actor, camx, camy, outline=""):
        x = actor["x"] - camx
        y = actor["y"] - camy
        r = actor["r"]

        self.cv.create_oval(x - r + 4, y - r + 8, x + r + 4, y + r + 8, fill=SHADOW, outline="")
        self.cv.create_oval(x - r, y - r, x + r, y + r, fill=actor["c"], outline=outline)

        fx = x + math.cos(actor["a"]) * r * 1.2
        fy = y + math.sin(actor["a"]) * r * 1.2
        self.cv.create_line(x, y, fx, fy, width=3)

    def draw(self):
        camx, camy = self.cam()
        self.cv.delete("all")
        self.cv.create_rectangle(0, 0, W, H, fill=FLOOR, outline="")

        sx, sy = -int(camx) % 60, -int(camy) % 60
        for x in range(sx, W + 60, 60):
            self.cv.create_line(x, 0, x, H, fill=GRID)
        for y in range(sy, H + 60, 60):
            self.cv.create_line(0, y, W, y, fill=GRID)

        for x, y, w, h in WALLS:
            self.cv.create_rectangle(x - camx, y - camy, x - camx + w, y - camy + h, fill=WALL, outline="")

        for actor in sorted([*self.enemies, self.p], key=lambda a: a["y"]):
            self.draw_actor(actor, camx, camy, "white" if actor is self.p else "")

        self.cv.create_text(14, 14, text="WASD move   R reset   ESC exit", fill=HUD, anchor="nw", font=("Arial", 12, "bold"))

    def tick(self):
        self.update_player()
        for enemy in self.enemies:
            self.update_enemy(enemy)
        self.draw()
        self.root.after(1000 // FPS, self.tick)

    def run(self):
        self.root.mainloop()
