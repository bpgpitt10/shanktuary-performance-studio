"""Tenth-pass shell: subtle sanctuary architecture without changing the product palette.

The sanctuary idea is treated as hidden structure, not a church costume:
- pointed-arch geometry is embedded in the app mark
- a ghost architectural frame lives behind the wordmark
- the existing graphite/navy + electric-blue + orange palette is preserved
- no serif/gold/ecclesiastical ornament is introduced
"""

from __future__ import annotations

import random

from PIL import Image, ImageDraw, ImageTk

import shell_redesign_v4 as v4
import shell_redesign_v7 as v7
import shell_redesign_v8 as v8
import theme

BLUE = v8.BLUE
BLUE_LINE = v8.BLUE_LINE
BLUE_TEXT = v8.BLUE_TEXT
ORANGE = getattr(theme, "WARN", "#FF7A32")
GOOD = getattr(theme, "GOOD", "#39A879")


def _mix(a, b, t):
    return v7._mix(a, b, t)


def _rgb(col):
    return tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))


def paint_nav(app, h):
    return v8.paint_nav(app, h)


def paint_sidebar(app, w, h):
    return v8.paint_sidebar(app, w, h)


def _brand_surface(app, w, h=52):
    """Equipment-dark header with architectural depth, not visible decoration."""
    key = (int(w), int(h))
    if getattr(app, "_brand_header_v10_key", None) == key:
        return app._brand_header_v10_img

    iw, ih = max(1, int(w)), max(1, int(h))
    img = Image.new("RGB", (iw, ih), _rgb("#07101A"))
    px = img.load()

    top = _rgb("#0D1A29")
    bottom = _rgb("#070B12")
    left = _rgb("#102238")
    right = _rgb("#070B11")

    # Multi-axis depth field. No radial glow / visible circle.
    for y in range(ih):
        ty = y / max(1, ih - 1)
        for x in range(iw):
            tx = x / max(1, iw - 1)
            brand_zone = max(0.0, 1.0 - x / 650.0)
            vals = []
            for i in range(3):
                vertical = top[i] + (bottom[i] - top[i]) * ty
                horizontal = left[i] + (right[i] - left[i]) * min(1.0, tx * 1.45)
                value = vertical * .58 + horizontal * .42
                if i == 2:
                    value += 3.2 * brand_zone * (1.0 - .35 * ty)
                elif i == 1:
                    value += 1.6 * brand_zone * (1.0 - .35 * ty)
                vals.append(max(0, min(255, round(value))))
            px[x, y] = tuple(vals)

    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(1027)

    # Very low-opacity material fibers / stone-like grain.
    for x in range(-ih, min(iw, 720), 17):
        d.line((x, ih, x + ih, 0), fill=(95, 145, 202, 6), width=1)
    for _ in range(120):
        x = rng.randrange(0, min(iw, 760))
        y = rng.randrange(0, ih)
        a = rng.randrange(3, 9)
        d.point((x, y), fill=(145, 177, 210, a))

    # Ghost sanctuary architecture: a broad pointed portal behind the lockup.
    # It is intentionally too faint to read as a literal church at a glance.
    arch_col = (79, 150, 255, 18)
    arch_col_inner = (117, 179, 255, 10)
    left_x, right_x, base_y = 48, 390, ih - 2
    apex_x, apex_y = 219, 1
    shoulder_y = 17
    d.line((left_x, base_y, left_x, shoulder_y), fill=arch_col, width=1)
    d.line((right_x, base_y, right_x, shoulder_y), fill=arch_col, width=1)
    d.line((left_x, shoulder_y, apex_x, apex_y), fill=arch_col, width=1)
    d.line((apex_x, apex_y, right_x, shoulder_y), fill=arch_col, width=1)

    inset = 10
    d.line((left_x + inset, base_y, left_x + inset, shoulder_y + 4), fill=arch_col_inner, width=1)
    d.line((right_x - inset, base_y, right_x - inset, shoulder_y + 4), fill=arch_col_inner, width=1)
    d.line((left_x + inset, shoulder_y + 4, apex_x, apex_y + 5), fill=arch_col_inner, width=1)
    d.line((apex_x, apex_y + 5, right_x - inset, shoulder_y + 4), fill=arch_col_inner, width=1)

    # A performance trace cuts across the architecture so the read remains golf-tech.
    trace = [(250, 42), (292, 39), (328, 31), (365, 22), (414, 19)]
    d.line(trace, fill=(74, 161, 255, 22), width=1)
    d.ellipse((411, 16, 416, 21), fill=(255, 124, 50, 48))

    d.line((0, 0, iw, 0), fill=(69, 142, 255, 14), width=1)
    d.line((0, ih - 1, iw, ih - 1), fill=(76, 116, 157, 34), width=1)

    app._brand_header_v10_img = ImageTk.PhotoImage(img)
    app._brand_header_v10_key = key
    return app._brand_header_v10_img


def _brand_mark(app):
    """Ownable Shanktuary mark: modern S inside a barely-there sanctuary portal."""
    if getattr(app, "_brand_mark_v10_img", None) is not None:
        return app._brand_mark_v10_img

    scale = 4
    w, h = 44, 44
    im = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")

    # Dark doorway body with a pointed top. This is the sanctuary reference.
    portal = [
        (5, 42), (5, 18), (7, 13), (12, 8), (22, 2),
        (32, 8), (37, 13), (39, 18), (39, 42),
    ]
    d.polygon([(x * scale, y * scale) for x, y in portal],
              fill=(8, 20, 34, 255), outline=(49, 126, 255, 255))

    # Electric-blue inner portal: architectural, but still obviously product-tech.
    inner = [
        (9, 40), (9, 19), (11, 15), (15, 11), (22, 7),
        (29, 11), (33, 15), (35, 19), (35, 40),
    ]
    d.line([(x * scale, y * scale) for x, y in inner],
           fill=(79, 157, 255, 180), width=1 * scale, joint="curve")

    # Small blue threshold makes the silhouette read as an opening, not a shield.
    d.line((9 * scale, 40 * scale, 35 * scale, 40 * scale),
           fill=(55, 129, 239, 145), width=1 * scale)

    # Chamfered S remains modern/performance-forward.
    white = (239, 247, 255, 255)
    pts = [
        (14, 12), (31, 12), (28, 16), (17, 16),
        (15, 18), (15, 21), (27, 21), (30, 24),
        (30, 29), (27, 32), (12, 32), (15, 28),
        (25, 28), (26, 27), (26, 25), (15, 25),
        (12, 22), (12, 17),
    ]
    d.polygon([(x * scale, y * scale) for x, y in pts], fill=white)

    # Orange impact point keeps the warm supporting accent in the identity.
    d.ellipse((29 * scale, 10 * scale, 33 * scale, 14 * scale),
              fill=(255, 124, 50, 255))

    im = im.resize((w, h), Image.Resampling.LANCZOS)
    app._brand_mark_v10_img = ImageTk.PhotoImage(im)
    return app._brand_mark_v10_img


def _utility_button(c, rect, text, active=False):
    if not rect:
        return
    x1, y1, x2, y2 = rect
    fill = _mix("#09111B", BLUE, .055 if active else .018)
    border = _mix(theme.HAIRLINE, BLUE_LINE, .16 if active else .05)
    c.create_rectangle(x1, y1, x2, y2, fill=fill, outline=border, width=1)
    if active:
        c.create_rectangle(x1, y1, x1 + 2, y2, fill=BLUE, outline="")
    c.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text,
                  fill=theme.TEXT if active else theme.TEXT_2,
                  font=(v4._font(), 10, "bold" if active else "normal"), anchor="center")


def paint_top_header(app, w, h, offset_x=0):
    c = app.canvas
    hh = 52
    c.create_image(0, 0, image=_brand_surface(app, w, hh), anchor="nw")

    # Integrated lockup. The sanctuary cue lives primarily in the mark; the
    # typography stays modern and in the palette already established for the app.
    c.create_image(10, 4, image=_brand_mark(app), anchor="nw")

    brand_x = 66
    c.create_text(brand_x, 7, text="SHANKTUARY", fill=theme.TEXT,
                  font=(v4._font(), 17, "bold"), anchor="nw")

    # Descriptor is part of the lockup, not a separate dashboard label.
    c.create_text(brand_x, 31, text="PERFORMANCE GOLF STUDIO",
                  fill=BLUE_TEXT, font=(v4._font(), 8, "bold"), anchor="nw")

    # One tiny architectural/golf signature: threshold line + impact point.
    line_y = 43
    c.create_line(brand_x, line_y, brand_x + 62, line_y,
                  fill=_mix(BLUE_LINE, theme.BG, .56), width=1)
    c.create_oval(brand_x + 64, line_y - 2, brand_x + 68, line_y + 2,
                  fill=ORANGE, outline="")
    c.create_line(brand_x + 70, line_y, brand_x + 129, line_y,
                  fill=_mix(BLUE_LINE, theme.BG, .56), width=1)

    # Utility cluster remains visually subordinate and operationally unchanged.
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
    c.create_oval(status_x, 23, status_x + 8, 31, fill=GOOD, outline="")
    c.create_text(status_x + 14, 27, text="Ready", fill=theme.TEXT_2,
                  font=(v4._font(), 9, "bold"), anchor="w")

    _utility_button(c, app.club_btn_rect,
                    f"{getattr(app, 'current_club', 'Club')}  ▼",
                    bool(getattr(app, "show_club_menu", False)))
    hand = "LH" if getattr(app, "is_left_handed", False) else "RH"
    _utility_button(c, app.dexterity_btn_rect, hand)
    _utility_button(c, app.tools_btn_rect, "Tools  ▼",
                    bool(getattr(app, "show_tools_menu", False)))
    _utility_button(c, app.fullscreen_btn_rect, "⛶")

    # Keep v8's design-owned click targets. This is important because the
    # production header paints first and mutates its own rectangles.
    app.design_club_btn_rect = tuple(app.club_btn_rect) if app.club_btn_rect else None
    app.design_dexterity_btn_rect = tuple(app.dexterity_btn_rect) if app.dexterity_btn_rect else None
    app.design_tools_btn_rect = tuple(app.tools_btn_rect) if app.tools_btn_rect else None
    app.design_fullscreen_btn_rect = tuple(app.fullscreen_btn_rect) if app.fullscreen_btn_rect else None
