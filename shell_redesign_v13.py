"""Gold/teal shell treatment for the isolated design sandbox.

Keeps v12 navigation hierarchy/gutter and v11 PNG branding geometry. Only the
header material and palette treatment change: antique gold is the primary
brand accent, with muted teal as the secondary technical/data cue.
"""

from __future__ import annotations

import random
from PIL import Image, ImageDraw, ImageTk

import shell_redesign_v9 as v9
import shell_redesign_v11 as v11
import shell_redesign_v12 as v12
import theme

NAV_RAIL_W = v12.NAV_RAIL_W
COLLAPSED_GUTTER_W = v12.COLLAPSED_GUTTER_W


def _rgb(col):
    return tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))


def _brand_surface(app, w, h=52):
    key = (int(w), int(h), "gold-teal-v1")
    if getattr(app, "_brand_header_v13_key", None) == key:
        return app._brand_header_v13_img

    iw, ih = max(1, int(w)), max(1, int(h))
    img = Image.new("RGB", (iw, ih), _rgb(theme.BG))
    px = img.load()

    top = _rgb("#102235")
    bottom = _rgb("#06101A")
    left = _rgb("#142A40")
    right = _rgb("#060D15")
    rng = random.Random(9147)

    for y in range(ih):
        ty = y / max(1, ih - 1)
        for x in range(iw):
            tx = x / max(1, iw - 1)
            vert = tuple(top[i] + (bottom[i] - top[i]) * ty for i in range(3))
            horiz = tuple(left[i] + (right[i] - left[i]) * min(1.0, tx * 1.45) for i in range(3))
            lift = max(0.0, 1.0 - x / 650.0) * (0.9 - 0.25 * ty)
            vals = []
            for i in range(3):
                v = vert[i] * .56 + horiz[i] * .44
                if i == 1:
                    v += 1.5 * lift
                elif i == 2:
                    v += 2.3 * lift
                vals.append(max(0, min(255, round(v))))
            px[x, y] = tuple(vals)

    d = ImageDraw.Draw(img, "RGBA")
    # Subtle woven/equipment texture: teal fibers, nearly invisible white cross fibers.
    for x in range(-ih, min(iw, 760), 13):
        d.line((x, ih, x + ih, 0), fill=(98, 169, 179, 7), width=1)
    for x in range(-ih, min(iw, 760), 19):
        d.line((x, 0, x + ih, ih), fill=(255, 255, 255, 4), width=1)

    # Technical launch traces: teal first, champagne-gold second, no orange.
    traces = [
        ((210, 43), (284, 38), (356, 15), (470, 21), (98, 169, 179, 20)),
        ((232, 45), (312, 40), (378, 25), (502, 30), (224, 184, 102, 14)),
        ((192, 39), (267, 35), (332, 28), (432, 33), (155, 110, 50, 10)),
    ]
    for p0, p1, p2, p3, col in traces:
        pts = []
        for step in range(61):
            t = step / 60.0
            mt = 1.0 - t
            x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
            y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
            pts.append((x, y))
        d.line(pts, fill=col, width=1)

    for x in (300, 350, 400, 450, 500):
        d.line((x, 43, x, 47), fill=(130, 172, 183, 12), width=1)
    for _ in range(24):
        x = rng.randint(175, min(max(176, iw - 1), 565))
        y = rng.randint(7, 46)
        r = rng.choice((1, 1, 1, 2))
        d.ellipse((x-r, y-r, x+r, y+r), fill=(164, 185, 186, rng.randint(4, 10)))

    d.line((0, 0, iw, 0), fill=(224, 184, 102, 15), width=1)
    d.line((0, ih - 1, iw, ih - 1), fill=(70, 116, 125, 32), width=1)

    app._brand_header_v13_img = ImageTk.PhotoImage(img)
    app._brand_header_v13_key = key
    return app._brand_header_v13_img


def paint_nav(app, h):
    return v12.paint_nav(app, h)


def paint_sidebar(app, w, h):
    return v12.paint_sidebar(app, w, h)


def paint_top_header(app, w, h, offset_x=0):
    c = app.canvas
    c.create_image(0, 0, image=_brand_surface(app, w, 52), anchor="nw")

    shield = v11._load_brand_image(app, "_brand_shield_v13_img", v11.SHIELD_PATH, 43)
    wordmark = v11._load_brand_image(app, "_brand_wordmark_v13_img", v11.WORDMARK_PATH, 39)
    if shield is not None:
        c.create_image(10, 4, image=shield, anchor="nw")
    if wordmark is not None:
        c.create_image(58, 7, image=wordmark, anchor="nw")

    right = w - 10
    y1, y2 = 7, 45
    fs_w, tools_w, dex_w, club_w, gap = 38, 86, 58, 112, 7

    app.fullscreen_btn_rect = (right - fs_w, y1, right, y2)
    right -= fs_w + gap
    app.tools_btn_rect = (right - tools_w, y1, right, y2)
    right -= tools_w + gap
    app.dexterity_btn_rect = (right - dex_w, y1, right, y2)
    right -= dex_w + gap
    app.club_btn_rect = (right - club_w, y1, right, y2)

    club_rect = app.club_btn_rect
    status_x = club_rect[0] - 82
    c.create_oval(status_x, 23, status_x + 8, 31, fill=theme.GOOD, outline="")
    c.create_text(status_x + 14, 27, text="Ready", fill=theme.TEXT_2,
                  font=(v9.v4._font(), 9, "bold"), anchor="w")

    v9._utility_button(c, app.club_btn_rect,
                       f"{getattr(app, 'current_club', 'Club')}  ▼",
                       bool(getattr(app, "show_club_menu", False)))
    hand = "LH" if getattr(app, "is_left_handed", False) else "RH"
    v9._utility_button(c, app.dexterity_btn_rect, hand)
    v9._utility_button(c, app.tools_btn_rect, "Tools  ▼",
                       bool(getattr(app, "show_tools_menu", False)))
    v9._utility_button(c, app.fullscreen_btn_rect, "⛶")

    app.design_club_btn_rect = tuple(app.club_btn_rect) if app.club_btn_rect else None
    app.design_dexterity_btn_rect = tuple(app.dexterity_btn_rect) if app.dexterity_btn_rect else None
    app.design_tools_btn_rect = tuple(app.tools_btn_rect) if app.tools_btn_rect else None
    app.design_fullscreen_btn_rect = tuple(app.fullscreen_btn_rect) if app.fullscreen_btn_rect else None
