import time
import tkinter as tk

from camera import Camera
from hud import draw_hud
from player import Player
from settings import CAMERA_SMOOTH, FPS, HEIGHT, TITLE, WALLS, WIDTH, WORLD_H, WORLD_W
from world import draw_actor, draw_floor, draw_walls


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

        self.last_fps_mark = time.perf_counter()
        self.frames = 0
        self.fps = 0

        self.tick()

    def _key_down(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = True

    def _key_up(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = False

    def _update_fps(self):
        self.frames += 1
        now = time.perf_counter()
        if now - self.last_fps_mark >= 1:
            self.fps = self.frames
            self.frames = 0
            self.last_fps_mark = now

    def tick(self):
        self.player.update(self.keys, WALLS, WORLD_W, WORLD_H)
        self.camera.update(self.player, WORLD_W, WORLD_H, CAMERA_SMOOTH)

        self.canvas.delete("all")
        draw_floor(self.canvas, self.camera)
        draw_walls(self.canvas, self.camera, WALLS)
        draw_actor(self.canvas, self.camera, self.player, outline="white")

        self._update_fps()
        draw_hud(self.canvas, self.fps, 0)
        self.root.after(int(1000 / FPS), self.tick)

    def run(self):
        self.root.mainloop()
