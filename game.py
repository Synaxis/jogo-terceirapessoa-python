import tkinter as tk

from camera import Camera
from player import Player
from settings import FPS, HEIGHT, TITLE, WIDTH, WORLD_H, WORLD_W
from world import draw_floor


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()

        self.keys = {k: False for k in "wasd"}
        self.root.bind("<KeyPress>", self._key_down)
        self.root.bind("<KeyRelease>", self._key_up)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        self.player = Player(120, 120)
        self.camera = Camera(WIDTH, HEIGHT)
        self.walls = []
        self.tick()

    def _key_down(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = True

    def _key_up(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = False

    def tick(self):
        self.player.update(self.keys, self.walls, WORLD_W, WORLD_H)
        self.camera.update(self.player, WORLD_W, WORLD_H, 0.14)

        self.canvas.delete("all")
        draw_floor(self.canvas, self.camera)

        sx = self.player.x - self.camera.x
        sy = self.player.y - self.camera.y
        r = self.player.size
        self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill=self.player.color, outline="white")

        self.root.after(int(1000 / FPS), self.tick)

    def run(self):
        self.root.mainloop()
