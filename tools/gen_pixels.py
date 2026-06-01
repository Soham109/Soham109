#!/usr/bin/env python3
"""Generate pixel-art PNG assets for the profile README."""
from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

SKY, SKY2 = (92, 148, 252), (68, 120, 220)
CLOUD = (240, 248, 255)
BRICK, BRICK_D = (180, 80, 40), (140, 55, 25)
GRASS, GRASS_D = (60, 180, 60), (40, 130, 40)
GOLD, GOLD_D = (255, 210, 60), (200, 150, 30)
WHITE, BLACK = (255, 255, 255), (25, 25, 45)
SKIN, SHIRT, PANTS, HAIR = (255, 200, 150), (60, 140, 255), (50, 50, 90), (60, 35, 20)
RED = (229, 37, 33)
BLUE = (60, 140, 255)
PURPLE = (120, 80, 180)


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/Library/Fonts/Courier New Bold.ttf",
    ]
    if not bold:
        candidates.reverse()
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def px(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, c: tuple[int, int, int]) -> None:
    draw.rectangle([x * s, y * s, (x + 1) * s - 1, (y + 1) * s - 1], fill=c)


def draw_cloud(draw: ImageDraw.ImageDraw, ox: int, oy: int, s: int) -> None:
    for dx, dy in [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1), (1, 2), (2, 2)]:
        px(draw, ox + dx, oy + dy, s, CLOUD)


def draw_brick(draw: ImageDraw.ImageDraw, ox: int, oy: int, s: int, q: bool = False) -> None:
    for row in range(4):
        for col in range(4):
            px(draw, ox + col, oy + row, s, BRICK if (row + col) % 2 == 0 else BRICK_D)
    if q:
        for x, y in [(1, 0), (2, 0), (2, 1), (1, 2), (1, 3)]:
            px(draw, ox + x, oy + y, s, GOLD_D)


def draw_hero(draw: ImageDraw.ImageDraw, ox: int, oy: int, s: int) -> None:
    rows = [
        "  HHHH  ",
        " HSSSSSH ",
        "HSSSSSSSH",
        " HHSSSHH ",
        "  TTTT  ",
        " TT  TT ",
        " PP  PP ",
        " PP  PP ",
    ]
    cmap = {"H": HAIR, "S": SKIN, "T": SHIRT, "P": PANTS}
    for row, line in enumerate(rows):
        for col, ch in enumerate(line):
            if ch != " ":
                px(draw, ox + col, oy + row, s, cmap[ch])


def banner() -> None:
    w, h, s = 960, 220, 4
    img = Image.new("RGB", (w, h), SKY)
    d = ImageDraw.Draw(img)
    for y in range(0, 44, 2):
        d.rectangle([0, y * s, w, (y + 1) * s], fill=SKY if y % 4 == 0 else SKY2)
    draw_cloud(d, 8, 3, s)
    draw_cloud(d, 55, 5, s)
    draw_cloud(d, 120, 2, s)
    draw_cloud(d, 180, 6, s)
    d.rectangle([0, 160, w, 176], fill=GRASS)
    d.rectangle([0, 176, w, h], fill=GRASS_D)
    draw_brick(d, 4, 38, s)
    draw_brick(d, 9, 38, s, True)
    draw_brick(d, 14, 38, s)
    draw_hero(d, 168, 33, s)
    d.ellipse([736, 142, 764, 170], fill=GOLD, outline=GOLD_D)
    d.rectangle([200, 48, 760, 152], fill=WHITE)
    d.rectangle([204, 52, 756, 148], fill=BLACK)
    d.text((480, 72), "SOHAM AGGARWAL", fill=GOLD, font=font(36), anchor="mm")
    d.text((480, 118), "CS + MATH  |  MARKETS  |  RISK  |  SYSTEMS", fill=WHITE, font=font(16), anchor="mm")
    img.save(os.path.join(OUT, "banner.png"), optimize=True)


def hud() -> None:
    w, h = 720, 88
    img = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=GOLD, width=3)
    d.rectangle([0, 0, w, 4], fill=GOLD)
    d.rectangle([0, h - 4, w, h], fill=GOLD_D)
    heart = [
        (20, 16), (28, 16), (36, 16),
        (12, 24), (20, 24), (28, 24), (36, 24), (44, 24),
        (20, 32), (28, 32), (36, 32), (28, 40),
    ]
    for x, y in heart:
        d.rectangle([x, y, x + 7, y + 7], fill=RED)
    d.text((58, 14), "PLAYER", fill=GOLD, font=font(12))
    d.text((58, 38), "UW-Madison '28", fill=WHITE, font=font(18))
    d.ellipse([268, 20, 292, 44], fill=GOLD, outline=GOLD_D)
    d.text((300, 14), "COINS", fill=GOLD, font=font(12))
    d.text((300, 38), "193 WPM", fill=WHITE, font=font(18))
    d.rectangle([500, 16, 532, 32], fill=GRASS)
    d.rectangle([516, 16, 532, 32], fill=GRASS_D)
    d.rectangle([500, 32, 532, 48], fill=GRASS_D)
    d.rectangle([516, 32, 532, 48], fill=GRASS)
    d.text((540, 14), "WORLD", fill=GOLD, font=font(12))
    d.text((540, 38), "Madison, WI", fill=WHITE, font=font(18))
    d.text((58, 72), "GPA 3.96 | Dean's List | CS & Math", fill=(136, 136, 136), font=font(11))
    d.text((540, 72), "TOP 0.44% TYPING", fill=(136, 136, 136), font=font(11))
    img.save(os.path.join(OUT, "hud.png"), optimize=True)


def divider() -> None:
    w, h, s = 800, 20, 4
    img = Image.new("RGB", (w, h), (13, 17, 23))
    d = ImageDraw.Draw(img)
    for x in range(w // s):
        px(d, x, 0, s, GRASS)
        px(d, x, 1, s, GRASS_D)
        for y in range(2, 5):
            px(d, x, y, s, BRICK if (x + y) % 2 == 0 else BRICK_D)
    img.save(os.path.join(OUT, "divider.png"), optimize=True)


def level_nse() -> None:
    w, h = 420, 100
    img = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=GOLD, width=3)
    draw_brick(d, 3, 3, 4)
    d.text((18, 38), "1-1", fill=GOLD, font=font(10))
    d.text((64, 22), "WORLD 1-1 | NSE CLEARING", fill=GOLD, font=font(18))
    d.text((64, 48), "Risk intern | max-flow collateral | 1M+ accounts", fill=(170, 170, 170), font=font(11))
    d.text((64, 68), "Dinic max-flow | graph pruning | Sharpe & Jensen's a", fill=WHITE, font=font(11))
    img.save(os.path.join(OUT, "level-nse.png"), optimize=True)


def level_lob() -> None:
    w, h = 420, 100
    img = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=BLUE, width=3)
    d.rectangle([12, 12, 52, 52], fill=BLUE)
    d.text((20, 38), "1-2", fill=WHITE, font=font(10))
    d.text((64, 22), "WORLD 1-2 | LOB FORECAST", fill=BLUE, font=font(18))
    d.text((64, 48), "Limit order book | microstructure | FI-2010", fill=(170, 170, 170), font=font(11))
    d.text((64, 68), "Spread | queue imbalance | microprice -> 0.841 F1 @ h3", fill=WHITE, font=font(11))
    img.save(os.path.join(OUT, "level-lob.png"), optimize=True)


def level_secret() -> None:
    w, h = 420, 100
    img = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=PURPLE, width=3)
    d.rectangle([12, 12, 52, 52], fill=PURPLE)
    d.text((16, 38), "???", fill=GOLD, font=font(10))
    d.text((64, 22), "SECRET WORLDS", fill=PURPLE, font=font(18))
    d.text((64, 48), "Side quests | smaller builds | still fun", fill=(170, 170, 170), font=font(11))
    d.text((64, 68), "Codebase RAG | CPOS | more on GitHub", fill=WHITE, font=font(11))
    d.rectangle([360, 48, 384, 88], fill=GRASS)
    d.rectangle([356, 44, 388, 56], fill=(80, 208, 80))
    img.save(os.path.join(OUT, "level-secret.png"), optimize=True)


def typing_card() -> None:
    w, h = 720, 120
    img = Image.new("RGB", (w, h), (13, 17, 23))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=GOLD, width=3)
    d.text((360, 22), "> HIGH SCORE TABLE <", fill=GOLD, font=font(14), anchor="mm")
    d.text((360, 48), "FASTESTTYPIST5", fill=WHITE, font=font(22), anchor="mm")
    bars = [
        (40, 66, "15s", 193, GOLD),
        (40, 86, "60s", 155, BLUE),
        (380, 66, "120s", 141, GRASS),
        (380, 86, "10w", 217, RED),
    ]
    for colx, y, lab, val, col in bars:
        d.text((colx, y + 12), lab, fill=(136, 136, 136), font=font(11))
        d.rectangle([colx + 40, y, colx + 40 + val, y + 16], fill=col)
        d.text((colx + 40 + val + 12, y + 12), str(val), fill=col, font=font(12))
    d.text(
        (360, 108),
        "3,435 tests | top 0.44% worldwide | monkeytype.com/profile/FastestTypist5",
        fill=(102, 102, 102),
        font=font(10),
        anchor="mm",
    )
    img.save(os.path.join(OUT, "typing.png"), optimize=True)


def trophy() -> None:
    w, h = 720, 72
    img = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=GOLD, width=2)
    d.text((360, 18), "ACHIEVEMENTS UNLOCKED", fill=GOLD, font=font(13), anchor="mm")
    d.text((360, 38), "BadgerAI '26 1st | Cursor Hacks '26 1st | UW Blockchain '25 2nd", fill=WHITE, font=font(11), anchor="mm")
    d.text(
        (360, 58),
        "2x AIME | IOQM top 10% | published ML research | ex tech lead Neuro86 @ MIT Media Lab",
        fill=(170, 170, 170),
        font=font(11),
        anchor="mm",
    )
    img.save(os.path.join(OUT, "trophy.png"), optimize=True)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    banner()
    hud()
    divider()
    level_nse()
    level_lob()
    level_secret()
    typing_card()
    trophy()
    for name in sorted(os.listdir(OUT)):
        if name.endswith(".png"):
            path = os.path.join(OUT, name)
            with Image.open(path) as im:
                print(f"{name}: {im.size[0]}x{im.size[1]} ({os.path.getsize(path) // 1024}K)")


if __name__ == "__main__":
    main()
