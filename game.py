import math
import tkinter as tk
from config import *

# verifica colisão entre círculo (objeto) e retângulo (parede)
def hit(x, y, r, wall):
    wx, wy, ww, wh = wall
    # encontra o ponto mais próximo do círculo dentro do retângulo
    nx = max(wx, min(x, wx + ww))
    ny = max(wy, min(y, wy + wh))
    # verifica distância ao quadrado
    return (x - nx) ** 2 + (y - ny) ** 2 < r * r

# move objeto com verificação de colisão e limites
def move(obj, dx, dy):
    # tentativa de movimento no eixo X
    x, y, r = obj["x"] + dx, obj["y"], obj["r"]
    if r <= x <= WORLD_W - r and not any(hit(x, y, r, w) for w in WALLS):
        obj["x"] = x

    # tentativa de movimento no eixo Y
    x, y = obj["x"], obj["y"] + dy
    if r <= y <= WORLD_H - r and not any(hit(x, y, r, w) for w in WALLS):
        obj["y"] = y

class Game:
    def __init__(self):
        # cria janela principal
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.resizable(False, False)

        # cria canvas (tela do jogo)
        self.cv = tk.Canvas(self.root, width=W, height=H, bg=BG, highlightthickness=0)
        self.cv.pack()

        # controle de teclas pressionadas
        self.keys = {k: 0 for k in "wasd"}
        self.root.bind("<KeyPress>", lambda e: self._set(e, 1))
        self.root.bind("<KeyRelease>", lambda e: self._set(e, 0))
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # sair do jogo
        self.root.bind("r", self.reset)  # resetar jogo

        self.reset()
        self.tick()

    # atualiza estado das teclas
    def _set(self, event, value):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = value

    # reinicia jogador e inimigos
    def reset(self, _=None):
        self.p = {"x": 120, "y": 120, "r": PLAYER_R, "a": 0.0, "c": PLAYER}
        self.enemies = [
            {"x": 760, "y": 380, "r": ENEMY_R, "a": 0.0, "c": ENEMY},
            {"x": 1410, "y": 540, "r": ENEMY_R, "a": 0.0, "c": ENEMY},
            {"x": 560, "y": 980, "r": ENEMY_R, "a": 0.0, "c": ENEMY},
        ]

    # calcula posição da câmera (segue jogador)
    def cam(self):
        x = max(0, min(WORLD_W - W, self.p["x"] - W / 2))
        y = max(0, min(WORLD_H - H, self.p["y"] - H / 2 + 80))
        return x, y

    # atualiza movimento do jogador
    def update_player(self):
        dx = self.keys["d"] - self.keys["a"]
        dy = self.keys["s"] - self.keys["w"]
        if dx or dy:
            # normaliza vetor para velocidade constante
            n = math.hypot(dx, dy)
            dx = dx / n * PLAYER_SPEED
            dy = dy / n * PLAYER_SPEED
            # calcula direção (ângulo)
            self.p["a"] = math.atan2(dy, dx)
            move(self.p, dx, dy)

    # IA simples: inimigo segue jogador
    def update_enemy(self, enemy):
        vx = self.p["x"] - enemy["x"]
        vy = self.p["y"] - enemy["y"]
        d = math.hypot(vx, vy)
        if d > 1:
            dx = vx / d * ENEMY_SPEED
            dy = vy / d * ENEMY_SPEED
            enemy["a"] = math.atan2(dy, dx)
            move(enemy, dx, dy)

    # desenha jogador ou inimigo
    def draw_actor(self, actor, camx, camy, outline=""):
        x = actor["x"] - camx
        y = actor["y"] - camy
        r = actor["r"]

        # sombra
        self.cv.create_oval(x - r + 4, y - r + 8, x + r + 4, y + r + 8, fill=SHADOW, outline="")
        # corpo
        self.cv.create_oval(x - r, y - r, x + r, y + r, fill=actor["c"], outline=outline)

        # linha indicando direção
        fx = x + math.cos(actor["a"]) * r * 1.2
        fy = y + math.sin(actor["a"]) * r * 1.2
        self.cv.create_line(x, y, fx, fy, width=3)

    # desenha tudo na tela
    def draw(self):
        camx, camy = self.cam()
        self.cv.delete("all")
        self.cv.create_rectangle(0, 0, W, H, fill=FLOOR, outline="")

        # desenha grid do chão
        sx, sy = -int(camx) % 60, -int(camy) % 60
        for x in range(sx, W + 60, 60):
            self.cv.create_line(x, 0, x, H, fill=GRID)
        for y in range(sy, H + 60, 60):
            self.cv.create_line(0, y, W, y, fill=GRID)

        # desenha paredes
        for x, y, w, h in WALLS:
            self.cv.create_rectangle(x - camx, y - camy, x - camx + w, y - camy + h, fill=WALL, outline="")

        # desenha atores ordenados por Y (efeito profundidade)
        for actor in sorted([*self.enemies, self.p], key=lambda a: a["y"]):
            self.draw_actor(actor, camx, camy, "white" if actor is self.p else "")

        # HUD (texto na tela)
        self.cv.create_text(14, 14, text="WASD move   R reset   ESC exit", fill=HUD, anchor="nw", font=("Arial", 12, "bold"))

    # loop principal do jogo
    def tick(self):
        self.update_player()
        for enemy in self.enemies:
            self.update_enemy(enemy)
        self.draw()
        self.root.after(1000 // FPS, self.tick)

    # inicia aplicação
    def run(self):
        self.root.mainloop()