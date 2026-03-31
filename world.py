import math

from settings import FLOOR, GRID, HEIGHT, PLAYER, SHADOW, WALL, WIDTH


def world_to_screen(cam, x, y):
    return x - cam.x, y - cam.y


def draw_floor(canvas, cam):
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=FLOOR, outline="")
    step = 60
    start_x = -int(cam.x) % step
    start_y = -int(cam.y) % step

    for x in range(start_x, WIDTH + step, step):
        canvas.create_line(x, 0, x, HEIGHT, fill=GRID)
    for y in range(start_y, HEIGHT + step, step):
        canvas.create_line(0, y, WIDTH, y, fill=GRID)


def draw_walls(canvas, cam, walls):
    for x, y, w, h in walls:
        sx, sy = world_to_screen(cam, x, y)
        if sx + w < 0 or sy + h < 0 or sx > WIDTH or sy > HEIGHT:
            continue
        canvas.create_rectangle(sx, sy, sx + w, sy + h, fill=WALL, outline="")


def draw_actor(canvas, cam, actor, outline=""):
    sx, sy = world_to_screen(cam, actor.x, actor.y)
    r = actor.size

    canvas.create_oval(sx - r + 4, sy - r + 8, sx + r + 4, sy + r + 8, fill=SHADOW, outline="")
    canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill=actor.color, outline=outline)

    fx = sx + math.cos(actor.angle) * r * 1.25
    fy = sy + math.sin(actor.angle) * r * 1.25
    canvas.create_line(sx, sy, fx, fy, width=3)

    if actor.color == PLAYER:
        canvas.create_arc(sx - r - 8, sy - r - 8, sx + r + 8, sy + r + 8, start=210, extent=120, style="arc", width=2)
