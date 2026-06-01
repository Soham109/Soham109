#!/usr/bin/env python3
"""Generate a cohesive set of pixel-art PNG assets for the GitHub profile README.

Technique: scenery is drawn on a small logical canvas (1 unit == 1 pixel-art
pixel) then upscaled with NEAREST so every pixel stays crisp. Text is drawn on a
separate full-resolution layer with the Press Start 2P bitmap font so it renders
sharp, then composited on top.
"""
from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "PressStart2P.ttf")

# ---- palette ---------------------------------------------------------------
SKY_HI = (120, 168, 255)
SKY = (92, 148, 252)
SKY_LO = (74, 128, 238)
CLOUD = (250, 252, 255)
CLOUD_SH = (196, 214, 255)
HILL = (64, 188, 92)
HILL_D = (40, 148, 64)
GRASS = (96, 208, 88)
GRASS_D = (56, 160, 64)
DIRT = (150, 92, 52)
DIRT_D = (118, 70, 38)
BRICK = (206, 102, 52)
BRICK_D = (156, 70, 32)
QBLOCK = (252, 200, 72)
QBLOCK_D = (210, 150, 36)
COIN = (252, 220, 96)
COIN_D = (224, 168, 40)
PIPE = (72, 196, 96)
PIPE_D = (40, 150, 70)
PANEL = (22, 22, 42)
PANEL_LO = (14, 14, 30)
GOLD = (255, 210, 78)
WHITE = (245, 247, 252)
GREY = (158, 162, 188)
RED = (228, 60, 56)
BLUE = (74, 144, 255)
PURPLE = (158, 110, 232)
GREEN = (86, 196, 110)
SKIN = (255, 200, 152)
SKIN_SH = (228, 160, 120)
HAIR = (74, 46, 28)
HOODIE = (66, 122, 232)
HOODIE_D = (44, 90, 188)
PANTS = (52, 56, 92)
SHOE = (40, 40, 50)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def new_scene(w: int, h: int, bg=SKY):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def upscale(img: Image.Image, s: int) -> Image.Image:
    return img.resize((img.width * s, img.height * s), Image.NEAREST)


def text_layer(w: int, h: int):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return layer, ImageDraw.Draw(layer)


def draw_text(d, xy, s, fill, size, anchor=None, shadow=None):
    if shadow is not None:
        d.text((xy[0] + 2, xy[1] + 2), s, fill=shadow, font=font(size), anchor=anchor)
    d.text(xy, s, fill=fill, font=font(size), anchor=anchor)


# ---- pixel primitives (operate on the small logical canvas) ----------------
def rect(d, x, y, w, h, c):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)


def sky_gradient(d, w, h):
    band = max(1, h // 3)
    rect(d, 0, 0, w, band, SKY_HI)
    rect(d, 0, band, w, band, SKY)
    rect(d, 0, 2 * band, w, h - 2 * band, SKY_LO)


def cloud(d, x, y):
    # puffy cloud ~ 22x9
    body = [
        "....XXXXXX....",
        "..XXXXXXXXXX..",
        ".XXXXXXXXXXXX.",
        "XXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXX",
    ]
    for ry, row in enumerate(body):
        for rx, ch in enumerate(row):
            if ch == "X":
                d.point((x + rx, y + ry), fill=CLOUD)
    for rx in range(14):
        d.point((x + rx, y + 5), fill=CLOUD_SH)


def hill(d, cx, base, r):
    for i in range(r):
        y = base - i
        half = r - i
        rect(d, cx - half, y, half * 2, 1, HILL)
    rect(d, cx - 2, base - r, 1, 1, HILL_D)


def bush(d, x, base):
    rect(d, x, base - 2, 10, 2, HILL_D)
    rect(d, x + 1, base - 4, 3, 2, HILL)
    rect(d, x + 5, base - 5, 3, 3, HILL)


def coin(d, x, y):
    art = [".XX.", "X..X", "X..X", "X..X", ".XX."]
    for ry, row in enumerate(art):
        for rx, ch in enumerate(row):
            if ch == "X":
                d.point((x + rx, y + ry), fill=COIN_D)
            else:
                if 0 < rx < 3:
                    d.point((x + rx, y + ry), fill=COIN)


def qblock(d, x, y):
    rect(d, x, y, 8, 8, QBLOCK)
    rect(d, x, y, 8, 1, QBLOCK_D)
    rect(d, x, y + 7, 8, 1, QBLOCK_D)
    rect(d, x, y, 1, 8, QBLOCK_D)
    rect(d, x + 7, y, 1, 8, QBLOCK_D)
    for px, py in [(3, 2), (4, 2), (4, 3), (3, 4), (3, 6)]:
        d.point((x + px, y + py), fill=QBLOCK_D)
    for cx, cy in [(1, 1), (6, 1), (1, 6), (6, 6)]:
        d.point((x + cx, y + cy), fill=QBLOCK_D)


def brick(d, x, y):
    rect(d, x, y, 8, 8, BRICK)
    for ry in range(0, 8, 2):
        rect(d, x, y + ry, 8, 1, BRICK_D)
    for ry in range(0, 8, 4):
        d.point((x + 3, y + ry), fill=BRICK_D)
        d.point((x + 7, y + ry + 2), fill=BRICK_D)


def ground(d, w, top, h):
    rect(d, 0, top, w, 2, GRASS)
    rect(d, 0, top + 2, w, 1, GRASS_D)
    rect(d, 0, top + 3, w, h - 3, DIRT)
    for x in range(0, w, 6):
        d.point((x, top + 5), fill=DIRT_D)
        d.point((x + 3, top + 7), fill=DIRT_D)


def pipe(d, x, base):
    top_w, body_w = 14, 10
    h = 14
    rect(d, x, base - h, top_w, 4, PIPE)
    rect(d, x, base - h, top_w, 1, (140, 230, 150))
    rect(d, x + (top_w - body_w) // 2, base - h + 4, body_w, h - 4, PIPE)
    rect(d, x + (top_w - body_w) // 2, base - h + 4, 1, h - 4, PIPE_D)


def hero(d, x, base):
    # original 16-wide developer/adventurer sprite, 22 tall, feet at `base`
    art = [
        "....HHHHHH....",
        "...HHHHHHHH...",
        "..HHSSSSSSHH..",
        "..HSSSSSSSSH..",
        "..SSKSSSSKSS..",  # eyes (K)
        "..SSSSSSSSSS..",
        "..SSSWWWWSSS..",  # mouth (W)
        "...SSSSSSSS...",
        "..BBBBBBBBBB..",
        ".BBBBBBBBBBBB.",
        "BB.BBBBBBBB.BB",
        "BB.BBBBBBBB.BB",
        "SS.BBBBBBBB.SS",  # hands (S) at sides
        "...BBBBBBBB...",
        "...BBB..BBB...",
        "...PPP..PPP...",
        "...PPP..PPP...",
        "...PPP..PPP...",
        "...PPP..PPP...",
        "..EEEE..EEEE..",
    ]
    cmap = {
        "H": HAIR,
        "S": SKIN,
        "K": (30, 30, 40),
        "W": (180, 90, 90),
        "B": HOODIE,
        "P": PANTS,
        "E": SHOE,
    }
    top = base - len(art)
    for ry, row in enumerate(art):
        for rx, ch in enumerate(row):
            if ch in cmap:
                d.point((x + rx, top + ry), fill=cmap[ch])
    # hoodie shading on right edge
    for ry in range(8, 14):
        d.point((x + 11, top + ry), fill=HOODIE_D)


def flag(d, x, base):
    h = 30
    rect(d, x, base - h, 1, h, (210, 215, 230))
    rect(d, x - 8, base - h, 8, 6, GREEN)
    d.point((x, base - h), fill=GOLD)


def panel(d, x, y, w, h, fill=PANEL, border=WHITE, inner=PANEL_LO):
    rect(d, x, y, w, h, border)
    rect(d, x + 1, y + 1, w - 2, h - 2, fill)
    rect(d, x + 2, y + 2, w - 4, h - 4, inner)


# ---- assets ----------------------------------------------------------------
def banner():
    S = 4
    W, H = 240, 78
    img, d = new_scene(W, H)
    sky_gradient(d, W, H)
    cloud(d, 14, 8)
    cloud(d, 96, 5)
    cloud(d, 180, 11)
    hill(d, 50, 60, 20)
    hill(d, 200, 60, 16)
    gtop = 60
    ground(d, W, gtop, H - gtop)
    bush(d, 120, gtop)
    bush(d, 158, gtop)
    qblock(d, 30, 26)
    brick(d, 38, 26)
    qblock(d, 46, 26)
    for i, cx in enumerate((33, 41, 49)):
        coin(d, cx + 1, 16)
    pipe(d, 214, gtop)
    flag(d, 196, gtop)
    hero(d, 14, gtop)
    big = upscale(img, S)

    # text sign panel drawn crisp at full res
    tl, td = text_layer(W * S, H * S)
    # panel box
    px0, py0, px1, py1 = 78 * S, 16 * S, 196 * S, 50 * S
    td.rectangle([px0 - 6, py0 - 6, px1 + 6, py1 + 6], fill=(245, 247, 252, 255))
    td.rectangle([px0 - 3, py0 - 3, px1 + 3, py1 + 3], fill=(22, 22, 42, 255))
    td.rectangle([px0, py0, px1, py1], fill=(14, 14, 30, 255))
    cx = (px0 + px1) // 2
    draw_text(td, (cx, py0 + 16 * 1.0), "SOHAM", GOLD, 30, anchor="mm", shadow=(0, 0, 0, 180))
    draw_text(td, (cx, py0 + 52), "AGGARWAL", GOLD, 30, anchor="mm", shadow=(0, 0, 0, 180))
    draw_text(td, (cx, py1 - 16), "MARKETS // RISK // SYSTEMS", WHITE, 11, anchor="mm")

    out = Image.alpha_composite(big.convert("RGBA"), tl).convert("RGB")
    out.save(os.path.join(OUT, "banner.png"), optimize=True)


def header(filename, label, accent, icon):
    """Slim section header bar: icon tile + label on a dark panel."""
    S = 4
    W, H = 200, 18
    img, d = new_scene(W, H, PANEL_LO)
    rect(d, 0, 0, W, 2, accent)
    rect(d, 0, H - 2, W, 2, accent)
    rect(d, 0, 0, 2, H, accent)
    rect(d, W - 2, 0, 2, H, accent)
    # icon tile
    rect(d, 8, 4, 10, 10, accent)
    rect(d, 9, 5, 8, 8, PANEL)
    big = upscale(img, S)
    tl, td = text_layer(W * S, H * S)
    draw_text(td, (14 * S, H * S // 2), icon, WHITE, 13, anchor="mm")
    draw_text(td, (26 * S, H * S // 2), label, accent, 15, anchor="lm")
    out = Image.alpha_composite(big.convert("RGBA"), tl).convert("RGB")
    out.save(os.path.join(OUT, filename), optimize=True)


def card(filename, accent, tag, title, line1, line2, icon):
    S = 4
    W, H = 116, 30
    img, d = new_scene(W, H, PANEL_LO)
    rect(d, 0, 0, W, H, accent)
    rect(d, 1, 1, W - 2, H - 2, PANEL)
    rect(d, 2, 2, W - 4, H - 4, PANEL_LO)
    # icon tile
    rect(d, 5, 6, 18, 18, accent)
    rect(d, 6, 7, 16, 16, PANEL)
    big = upscale(img, S)
    tl, td = text_layer(W * S, H * S)
    draw_text(td, (14 * S, 15 * S), icon, WHITE, 18, anchor="mm")
    draw_text(td, (28 * S, 7 * S), tag, accent, 9, anchor="lm")
    draw_text(td, (28 * S, 14 * S), title, WHITE, 13, anchor="lm")
    draw_text(td, (28 * S, 21 * S), line1, GREY, 8, anchor="lm")
    draw_text(td, (28 * S, 26 * S), line2, GREY, 8, anchor="lm")
    out = Image.alpha_composite(big.convert("RGBA"), tl).convert("RGB")
    out.save(os.path.join(OUT, filename), optimize=True)


def typing():
    S = 4
    W, H = 200, 40
    img, d = new_scene(W, H, PANEL_LO)
    rect(d, 0, 0, W, 2, GOLD)
    rect(d, 0, H - 2, W, 2, COIN_D)
    rect(d, 0, 0, 2, H, GOLD)
    rect(d, W - 2, 0, 2, H, GOLD)
    for i, c in enumerate((GOLD, BLUE, GREEN, RED)):
        coin(d, 6 + i * 6, 6)
    big = upscale(img, S)
    tl, td = text_layer(W * S, H * S)
    draw_text(td, (W * S // 2, 6 * S), "HIGH SCORES", GOLD, 12, anchor="mm")
    rows = [("15s", 193, GOLD), ("60s", 155, BLUE), ("120s", 141, GREEN), ("10w", 217, RED)]
    colx = [14, 110]
    maxw = 70 * S
    for i, (lab, val, col) in enumerate(rows):
        col_i = i // 2
        row_i = i % 2
        bx = colx[col_i] * S
        by = (15 + row_i * 9) * S
        draw_text(td, (bx, by + 3 * S), lab, GREY, 8, anchor="lm")
        bar_x = bx + 22 * S
        bar_w = int((val / 217) * (maxw - 24 * S))
        td.rectangle([bar_x, by, bar_x + bar_w, by + 6 * S], fill=col + (255,))
        draw_text(td, (bar_x + bar_w + 4, by + 3 * S), str(val), col, 9, anchor="lm")
    draw_text(td, (W * S // 2, (H - 4) * S), "3,435 TESTS  //  TOP 0.44% WORLDWIDE", GREY, 7, anchor="mm")
    out = Image.alpha_composite(big.convert("RGBA"), tl).convert("RGB")
    out.save(os.path.join(OUT, "typing.png"), optimize=True)


def trophy():
    S = 4
    W, H = 200, 22
    img, d = new_scene(W, H, PANEL_LO)
    rect(d, 0, 0, W, 2, GOLD)
    rect(d, 0, H - 2, W, 2, COIN_D)
    big = upscale(img, S)
    tl, td = text_layer(W * S, H * S)
    draw_text(td, (W * S // 2, 6 * S), "ACHIEVEMENTS UNLOCKED", GOLD, 10, anchor="mm")
    draw_text(td, (W * S // 2, 13 * S), "BadgerAI 1st  //  Cursor Hacks 1st  //  UW Blockchain 2nd", WHITE, 7, anchor="mm")
    draw_text(td, (W * S // 2, 18 * S), "2x AIME  //  IOQM top 10%  //  published ML research", GREY, 7, anchor="mm")
    out = Image.alpha_composite(big.convert("RGBA"), tl).convert("RGB")
    out.save(os.path.join(OUT, "trophy.png"), optimize=True)


def divider():
    S = 4
    W, H = 200, 6
    img, d = new_scene(W, H, (13, 17, 23))
    rect(d, 0, 0, W, 2, GRASS)
    rect(d, 0, 2, W, 1, GRASS_D)
    for x in range(W):
        d.point((x, 3), fill=BRICK if x % 2 == 0 else BRICK_D)
        d.point((x, 4), fill=BRICK_D if x % 2 == 0 else BRICK)
    upscale(img, S).save(os.path.join(OUT, "divider.png"), optimize=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    banner()
    header("hdr-about.png", "PLAYER PROFILE", GOLD, "@")
    header("hdr-quests.png", "MAIN QUESTS", RED, "!")
    header("hdr-projects.png", "SIDE QUESTS", PURPLE, "*")
    header("hdr-scores.png", "HIGH SCORES", BLUE, "#")
    header("hdr-inventory.png", "INVENTORY", GREEN, "+")
    header("hdr-trophies.png", "TROPHIES", GOLD, "^")
    card("card-nse.png", RED, "WORLD 1-1", "NSE CLEARING", "Risk intern - max-flow collateral", "1M+ accounts - Sharpe & Jensen alpha", "$")
    card("card-lob.png", BLUE, "WORLD 1-2", "LOB FORECAST", "Market microstructure - FI-2010", "queue imbalance -> 0.841 F1 @ h3", "~")
    card("card-rag.png", PURPLE, "BONUS", "CODEBASE RAG", "Chat with any repo", "embeddings + cosine + LLM", "?")
    card("card-cpos.png", GREEN, "BONUS", "CPOS", "Competitive programming TUI", "side project", ">")
    typing()
    trophy()
    divider()
    for name in sorted(os.listdir(OUT)):
        if name.endswith(".png"):
            p = os.path.join(OUT, name)
            with Image.open(p) as im:
                print(f"{name}: {im.size[0]}x{im.size[1]} ({os.path.getsize(p)//1024}K)")


if __name__ == "__main__":
    main()
