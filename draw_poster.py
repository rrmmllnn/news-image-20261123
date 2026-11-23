#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news broadsheet poster.

Renders a 1024x1024 front-page poster with PIL and writes entry.png
next to this script. Run: python3 draw_poster.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (247, 243, 234)
INK = (22, 28, 38)
NAVY = (20, 32, 58)
RED = (193, 39, 45)
GOLD = (214, 158, 46)
CARD = (255, 255, 255)
CARD_LINE = (216, 210, 196)
MUTED = (92, 96, 104)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced_text(draw, cx, y, text, fnt, fill, tracking=4):
    """Draw centred text with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def chip(draw, x, y, label, bg, fg=(255, 255, 255)):
    fnt = font(SANS_B, 17)
    tw = draw.textlength(label, font=fnt)
    pad = 10
    draw.rounded_rectangle([x, y, x + tw + pad * 2, y + 26],
                           radius=4, fill=bg)
    draw.text((x + pad, y + 4), label, font=fnt, fill=fg)
    return tw + pad * 2


def icon_globe(draw, cx, cy, r, col):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=col, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=col, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             200, 340, fill=col, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             20, 160, fill=col, width=3)
    draw.line([cx + r * 0.55, cy - r * 0.75, cx + r * 0.2, cy - r * 0.2],
              fill=RED, width=5)
    draw.line([cx + r * 0.2, cy - r * 0.2, cx + r * 0.55, cy + r * 0.3],
              fill=RED, width=5)


def icon_tanker(draw, cx, cy, col):
    draw.polygon([(cx - 46, cy + 8), (cx + 46, cy + 8), (cx + 36, cy + 30),
                  (cx - 36, cy + 30)], fill=col)
    draw.rectangle([cx + 18, cy - 16, cx + 38, cy + 8], fill=col)
    draw.rectangle([cx + 24, cy - 26, cx + 28, cy - 16], fill=col)
    draw.rectangle([cx - 36, cy - 6, cx - 20, cy + 8], fill=col)
    draw.arc([cx - 46, cy + 36, cx - 12, cy + 54], 180, 360,
             fill=col, width=4)
    draw.arc([cx + 2, cy + 36, cx + 36, cy + 54], 180, 360,
             fill=col, width=4)


def icon_drone(draw, cx, cy, col):
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=col)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        rx, ry = cx + sx * 30, cy + sy * 22
        draw.line([cx, cy, rx, ry], fill=col, width=4)
        draw.ellipse([rx - 12, ry - 4, rx + 12, ry + 4], fill=col)
    draw.arc([cx - 44, cy + 34, cx - 10, cy + 56], 180, 360,
             fill=col, width=4)
    draw.arc([cx + 10, cy + 34, cx + 44, cy + 56], 180, 360,
             fill=col, width=4)


def icon_flats(draw, cx, cy, col):
    draw.rectangle([cx - 42, cy - 34, cx + 42, cy + 40], fill=col)
    for gy in (-22, 0, 22):
        for gx in (-30, -2, 26):
            draw.rectangle([cx + gx - 7, cy + gy - 7, cx + gx + 7,
                            cy + gy + 7], fill=PAPER)
    draw.line([cx + 18, cy - 34, cx + 42, cy - 8], fill=RED, width=5)
    draw.line([cx + 42, cy - 8, cx + 26, cy + 12], fill=RED, width=5)


def icon_planet(draw, cx, cy, col):
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=col)
    for dx, dy, r in ((-14, -8, 6), (10, 6, 8), (2, -18, 5), (-4, 16, 4)):
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=(255, 255, 255))
    draw.arc([cx - 46, cy - 20, cx + 46, cy + 20], 195, 345,
             fill=GOLD, width=5)


def icon_trophy(draw, cx, cy, col):
    draw.polygon([(cx - 30, cy - 34), (cx + 30, cy - 34), (cx + 22, cy + 2),
                  (cx - 22, cy + 2)], fill=col)
    draw.arc([cx - 46, cy - 38, cx - 16, cy + 2], 90, 270,
             fill=col, width=5)
    draw.arc([cx + 16, cy - 38, cx + 46, cy + 2], 270, 90,
             fill=col, width=5)
    draw.rectangle([cx - 6, cy + 2, cx + 6, cy + 22], fill=col)
    draw.rectangle([cx - 22, cy + 22, cx + 22, cy + 34], fill=col)


def icon_flame(draw, cx, cy, col):
    draw.polygon([(cx, cy - 48), (cx + 26, cy - 6), (cx + 34, cy + 14),
                  (cx + 16, cy + 38), (cx - 16, cy + 38), (cx - 34, cy + 14),
                  (cx - 26, cy - 6)], fill=col)
    draw.ellipse([cx - 12, cy + 6, cx + 12, cy + 34], fill=GOLD)


def icon_castle(draw, cx, cy, col):
    draw.rectangle([cx - 30, cy + 10, cx + 30, cy + 40], fill=col)
    draw.polygon([(cx - 44, cy + 12), (cx + 44, cy + 12), (cx + 32, cy - 6),
                  (cx - 32, cy - 6)], fill=col)
    draw.rectangle([cx - 22, cy - 26, cx + 22, cy - 6], fill=col)
    draw.polygon([(cx - 36, cy - 4), (cx + 36, cy - 4), (cx + 24, cy - 20),
                  (cx - 24, cy - 20)], fill=col)
    draw.rectangle([cx - 14, cy - 38, cx + 14, cy - 20], fill=col)
    draw.polygon([(cx - 26, cy - 18), (cx + 26, cy - 18), (cx + 16, cy - 32),
                  (cx - 16, cy - 32)], fill=col)
    draw.rectangle([cx - 2, cy - 46, cx + 2, cy - 32], fill=col)
    draw.rectangle([cx - 7, cy + 20, cx + 7, cy + 40], fill=PAPER)


def icon_doc(draw, cx, cy, col):
    draw.rectangle([cx - 32, cy - 42, cx + 32, cy + 42], outline=col, width=4)
    draw.polygon([(cx + 12, cy - 42), (cx + 32, cy - 22), (cx + 32, cy - 42)],
                 fill=col)
    for i, yy in enumerate((-18, 0, 18)):
        draw.line([cx - 20, cy + yy, cx + 20 - (8 if i == 2 else 0), cy + yy],
                  fill=col, width=4)
    draw.line([cx - 26, cy - 30, cx + 26, cy + 30], fill=RED, width=6)
    draw.line([cx + 26, cy - 30, cx - 26, cy + 30], fill=RED, width=6)


ICONS = {
    "globe": icon_globe,
    "tanker": icon_tanker,
    "drone": icon_drone,
    "flats": icon_flats,
    "planet": icon_planet,
    "trophy": icon_trophy,
    "flame": icon_flame,
    "castle": icon_castle,
    "doc": icon_doc,
}

CARDS = [
    ("HORMUZ", (178, 34, 34), "tanker",
     "OIL TANKERS STRUCK IN HORMUZ",
     "Strikes and mines hit shipping in the Strait as the war reaches Saudi Arabia and Bahrain."),
    ("LIBYA", (28, 60, 110), "drone",
     "SEA DRONES SINK RUSSIAN WARSHIP",
     "Suspected Ukrainian drones hit the corvette Merkury at Benghazi; the ship capsized."),
    ("UKRAINE", (146, 96, 8), "flats",
     "DRONE HITS FLATS NEAR KYIV",
     "Two killed, 11 missing \u2014 among them two children \u2014 after a strike on a block in Dymer."),
    ("SPACE", (84, 48, 130), "planet",
     "BEPICOLOMBO REACHES MERCURY",
     "After an eight-year voyage the probe enters orbit \u2014 only the second mission ever to do so."),
    ("SPORT", (24, 110, 60), "trophy",
     "LIVERPOOL ROUT MAN UTD",
     "Ten-man United beaten in Pochettino\u2019s debut; India post a record 720/9 in Wellington."),
    ("INDONESIA", (196, 92, 20), "flame",
     "FACTORY FIRE: DOZENS MISSING",
     "Blaze at a candy factory in Cikande, Banten; three confirmed dead, search under way."),
    ("JAPAN", (14, 120, 118), "castle",
     "SHURI CASTLE RISES AGAIN",
     "Okinawa celebrates the restored main hall, seven years after fire destroyed it."),
    ("SOUTH KOREA", (70, 80, 96), "doc",
     "MINISTER QUITS OVER AI CHEATING",
     "South Korea\u2019s education minister resigns amid an AI exam-cheating scandal."),
]


def draw_card(draw, x, y, w, h, kicker, color, icon, headline, summary):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8,
                           fill=CARD, outline=CARD_LINE, width=1)
    chip(draw, x + 14, y + 10, kicker, color)
    icon_cx, icon_cy = x + w - 48, y + 44
    ICONS[icon](draw, icon_cx, icon_cy, color)
    head_f = font(SANS_B, 24)
    text_w = w - 28 - 96
    lines = wrap(draw, headline, head_f, text_w)
    ty = y + 42
    for line in lines[:2]:
        draw.text((x + 14, ty), line, font=head_f, fill=INK)
        ty += 28
    sum_f = font(SANS, 17)
    slines = wrap(draw, summary, sum_f, w - 28)
    sy = ty + 4
    for line in slines[:2]:
        draw.text((x + 14, sy), line, font=sum_f, fill=MUTED)
        sy += 20


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead band
    draw.rectangle([0, 0, W, 132], fill=NAVY)
    title_f = font(SERIF, 62)
    draw.text((W // 2, 18), "THE WORLD IN ONE DAY", font=title_f,
              fill=(255, 255, 255), anchor="ma")
    spaced_text(draw, W // 2, 92, "MONDAY 23 NOVEMBER 2026",
                font(SANS_B, 25), GOLD, tracking=6)
    draw.rectangle([0, 132, W, 138], fill=RED)

    # Lead story: COP31
    ly = 150
    chip(draw, MARGIN, ly, "LEAD  \u2022  CLIMATE", RED)
    lead_f = font(SERIF, 50)
    draw.text((MARGIN, ly + 36), "COP31 CLIMATE", font=lead_f, fill=INK)
    draw.text((MARGIN, ly + 92), "TALKS COLLAPSE", font=lead_f, fill=INK)
    deck_f = font(SANS, 22)
    deck = ("No deal on fossil fuels as the EU and others reject the final "
            "draft \u2014 the talks end in failure.")
    dlines = wrap(draw, deck, deck_f, 560)
    dy = ly + 154
    for line in dlines[:2]:
        draw.text((MARGIN, dy), line, font=deck_f, fill=MUTED)
        dy += 27
    draw.ellipse([812, 172, 956, 316], outline=NAVY, width=2)
    icon_globe(draw, 884, 244, 58, NAVY)
    draw.text((884, 322), "THE PLANET WAITS", font=font(SANS_B, 15),
              fill=MUTED, anchor="ma")

    # Divider
    draw.line([MARGIN, 366, W - MARGIN, 366], fill=CARD_LINE, width=2)

    # Card grid: 2 columns x 4 rows
    gx, gy = MARGIN, 378
    cw = (W - 2 * MARGIN - 16) // 2
    ch = 144
    for i, (kicker, color, icon, headline, summary) in enumerate(CARDS):
        cx = gx + (i % 2) * (cw + 16)
        cy = gy + (i // 2) * (ch + 10)
        draw_card(draw, cx, cy, cw, ch, kicker, color, icon, headline,
                  summary)

    # Footer
    fy = 992
    draw.line([MARGIN, fy, W - MARGIN, fy], fill=CARD_LINE, width=1)
    foot_f = font(SANS, 16)
    draw.text((W // 2, fy + 8),
              "Compiled from wire reports  \u2022  AP  \u2022  Reuters  \u2022  BBC  \u2022  "
              "Al Jazeera  \u2022  The Hindu",
              font=foot_f, fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
