"""Eleventh-pass shell: finalized sanctuary lockup with quieter controls."""

from __future__ import annotations

import tkinter.font as tkfont

from PIL import Image, ImageDraw, ImageTk

import shell_redesign_v10 as v10
import shell_redesign_v4 as v4
import theme

BLUE = v10.BLUE
BLUE_LINE = v10.BLUE_LINE
BLUE_TEXT = v10.BLUE_TEXT
ORANGE = v10.ORANGE
GOOD = v10.GOOD


def paint_nav(app, h):
    return v10.paint_nav(app, h)


def paint_sidebar(app, w, h):
    return v10.paint_sidebar(app, w, h)


def _brand_mark(app):
    """Sanctuary portal mark with the S visually centered lower in the opening."""
    if getattr(app, "_brand_mark_v11_img", None) is not None:
        return app._brand_mark_v11_img

    scale = 4
    w, h = 44, 44
    im = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")

    portal = [
        (5, 42), (5, 18), (7, 13), (12, 8), (22, 2),
        (32, 8), (37, 13), (39, 18), (39, 42),
    ]
    d.polygon([(x * scale, y * scale) for x, y in portal],
              fill=(8, 20, 34, 255), outline=(49, 126, 255, 255))

    inner = [
        (9, 40), (9, 19), (11, 15), (15, 11), (22, 7),
        (29, 11), (33, 15), (35, 19), (35, 40),
    ]
    d.line([(x * scale, y * scale) for x, y in inner],
           fill=(79, 157, 255, 180), width=1 * scale, joint="curve")
    d.line((9 * scale, 40 * scale, 35 * scale, 40 * scale),
           fill=(55, 129, 239, 145), width=1 * scale)

    # Same accepted chamfered S, shifted down 2px for optical centering.
    white = (239, 247, 255, 255)
    pts = [
        (14, 14), (31, 14), (28, 18), (17, 18),
        (15, 20), (15, 23), (27, 23), (30, 26),
        (30, 31), (27, 34), (12, 34), (15, 30),
        (25, 30), (26, 29), (26, 27), (15, 27),
        (12, 24), (12, 19),
    ]
    d.polygon([(x * scale, y * scale) for x, y in pts], fill=white)
    d.ellipse((29 * scale, 12 * scale, 33 * scale, 16 * scale),
              fill=(255, 124, 50, 255))

    im = im.resize((w, h), Image.Resampling.LANCZOS)
    app._brand_mark_v11_img = ImageTk.PhotoImage(im)
    return app._brand_mark_v11_img


def _measure(text, family, size, weight="bold"):
    try:
        return tkfont.Font(family=family, size=size, weight=weight).measure(text)
    except Exception:
        return int(len(text) * size * .62)


def _inflate(rect, px=4, py=4, left_bound=0, top_bound=0, right_bound=None, bottom_bound=None):
    if not rect:
        return None
    x1, y1, x2, y2 = rect
    x1, y1, x2, y2 = x1 - px, y1 - py, x2 + px, y2 + py
    x1, y1 = max(left_bound, x1), max(top_bound, y1)
    if right_bound is not None:
        x2 = min(right_bound, x2)
    if bottom_bound is not None:
        y2 = min(bottom_bound, y2)
    return (x1, y1, x2, y2)


def paint_top_header(app, w, h, offset_x=0):
    c = app.canvas
    hh = 52
    c.create_image(0, 0, image=v10._brand_surface(app, w, hh), anchor="nw")
    c.create_image(10, 4, image=_brand_mark(app), anchor="nw")

    brand_x = 61
    family = v4._font()
    size = 17
    word = "SHANKTUARY"
    word_id = c.create_text(brand_x, 7, text=word, fill=theme.TEXT,
                            font=(family, size, "bold"), anchor="nw")
    bb = c.bbox(word_id)
    word_right = bb[2] if bb else brand_x + _measure(word, family, size)
    word_center = (brand_x + word_right) / 2

    # Turn the existing T into a subtle cross by extending only its stem above
    # the cap height. It reads as a typographic quirk first, sanctuary cue second.
    pre_w = _measure("SHANK", family, size)
    t_w = _measure("T", family, size)
    t_center = brand_x + pre_w + t_w / 2
    c.create_line(t_center, 2, t_center, 10, fill=theme.TEXT, width=2)

    # Descriptor is optically centered beneath the wordmark, not left-aligned.
    c.create_text(word_center, 31, text="PERFORMANCE GOLF STUDIO",
                  fill=BLUE_TEXT, font=(family, 8, "bold"), anchor="n")

    # Short signature rule around the orange impact point.
    line_y = 44
    dot_x = word_center
    c.create_line(dot_x - 44, line_y, dot_x - 9, line_y,
                  fill=v10._mix(BLUE_LINE, theme.BG, .48), width=1)
    c.create_oval(dot_x - 3, line_y - 3, dot_x + 3, line_y + 3,
                  fill=ORANGE, outline="")
    c.create_line(dot_x + 9, line_y, dot_x + 44, line_y,
                  fill=v10._mix(BLUE_LINE, theme.BG, .48), width=1)

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

    status_x = app.club_btn_rect[0] - 82
    c.create_oval(status_x, 23, status_x + 8, 31, fill=GOOD, outline="")
    c.create_text(status_x + 14, 27, text="Ready", fill=theme.TEXT_2,
                  font=(family, 9, "bold"), anchor="w")

    v10._utility_button(c, app.club_btn_rect,
                        f"{getattr(app, 'current_club', 'Club')}  ▼",
                        bool(getattr(app, "show_club_menu", False)))
    hand = "LH" if getattr(app, "is_left_handed", False) else "RH"
    v10._utility_button(c, app.dexterity_btn_rect, hand)
    v10._utility_button(c, app.tools_btn_rect, "Tools  ▼",
                        bool(getattr(app, "show_tools_menu", False)))
    v10._utility_button(c, app.fullscreen_btn_rect, "⛶")

    # Freeze slightly larger design-owned targets. Gaps remain between controls,
    # so forgiveness never causes one button to steal a neighbour's click.
    app.design_club_btn_rect = _inflate(app.club_btn_rect, 3, 4, right_bound=w, bottom_bound=hh)
    app.design_dexterity_btn_rect = _inflate(app.dexterity_btn_rect, 3, 4, right_bound=w, bottom_bound=hh)
    app.design_tools_btn_rect = _inflate(app.tools_btn_rect, 3, 4, right_bound=w, bottom_bound=hh)
    app.design_fullscreen_btn_rect = _inflate(app.fullscreen_btn_rect, 3, 4, right_bound=w, bottom_bound=hh)
