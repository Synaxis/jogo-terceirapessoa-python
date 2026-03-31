from settings import HUD


def draw_hud(canvas, fps, enemy_count):
    text = f"WASD move  R reset  ESC exit   FPS {fps}   NPC {enemy_count}"
    canvas.create_text(16, 16, text=text, fill=HUD, anchor="nw", font=("Arial", 13, "bold"))
