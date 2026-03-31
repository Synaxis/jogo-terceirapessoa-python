from settings import HEIGHT, WIDTH


def draw_floor(canvas, cam):
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#2b3240", outline="")
    step = 60
    start_x = -int(cam.x) % step
    start_y = -int(cam.y) % step

    for x in range(start_x, WIDTH + step, step):
        canvas.create_line(x, 0, x, HEIGHT, fill="#384154")
    for y in range(start_y, HEIGHT + step, step):
        canvas.create_line(0, y, WIDTH, y, fill="#384154")


def draw_walls(canvas, cam, walls):
    for x, y, w, h in walls:
        sx = x - cam.x
        sy = y - cam.y
        canvas.create_rectangle(sx, sy, sx + w, sy + h, fill="#98a2b3", outline="")
