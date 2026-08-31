"""Twelfth-pass shell: grouped one-word navigation hierarchy."""

import shell_redesign as icons
import shell_redesign_v7 as v7
import shell_redesign_v11 as v11
import theme

BLUE = v11.BLUE
BLUE_LINE = v11.BLUE_LINE


def _mix(a, b, t):
    return v11.v10._mix(a, b, t)


def _setup_icon(c, cx, cy, col):
    for dy, knob in ((-6, -3), (0, 4), (6, 0)):
        c.create_line(cx - 10, cy + dy, cx + 10, cy + dy, fill=col, width=1)
        c.create_oval(cx + knob - 2, cy + dy - 2, cx + knob + 2, cy + dy + 2,
                      fill=col, outline="")


def _group_label(c, y, text):
    c.create_text(theme.RAIL_W / 2, y, text=text, fill=_mix(theme.TEXT_3, theme.BG, .12),
                  font=(theme.ui_font(), 6, "bold"), anchor="n")


def _nav_item(app, y, mode_id, display, icon_kind=None, h=42):
    c = app.canvas
    rw = theme.RAIL_W
    active = app.view_mode == mode_id
    rect = (0, y - 2, rw, y + h + 2)
    app.mode_pill_rects[mode_id] = rect
    app.design_mode_rects[mode_id] = rect

    if active:
        c.create_rectangle(5, y, rw - 5, y + h, fill=_mix(theme.SURFACE_2, BLUE, .11), outline="")
        c.create_rectangle(5, y, 8, y + h, fill=BLUE, outline="")

    col = theme.TEXT if active else theme.TEXT_3
    icon_col = BLUE_LINE if active else _mix(theme.TEXT_3, theme.TEXT_2, .32)
    cy = y + 14
    if display == "Setup":
        _setup_icon(c, 32, cy, icon_col)
    else:
        icons._draw_nav_icon(c, icon_kind or display, 32, cy, icon_col)
    c.create_text(32, y + 34, text=display, fill=col,
                  font=(theme.ui_font(), 7, "bold" if active else "normal"), anchor="center")
    return y + h + 3


def paint_nav(app, h):
    """Session review first, Range isolated as Practice, utilities grouped as Tools."""
    c = app.canvas
    rw = theme.RAIL_W
    shell_bg = _mix(theme.RAIL, theme.BG, .42)
    c.create_rectangle(0, 0, rw, h, fill=shell_bg, outline="")
    c.create_line(rw - 1, 0, rw - 1, h, fill=_mix(theme.HAIRLINE, theme.BG, .46))

    app.mode_pill_rects = {}
    app.design_mode_rects = {}

    y = 62
    _group_label(c, y, "SESSION")
    y += 14
    for mode_id, display, icon_kind in (
        (9, "Shot", "Overview"),
        (1, "Club", "Quad"),
        (3, "Dispersion", "Disp"),
        (4, "Table", "Table"),
        (5, "Numbers", "Nums"),
    ):
        y = _nav_item(app, y, mode_id, display, icon_kind)

    y += 7
    _group_label(c, y, "PRACTICE")
    y += 14
    y = _nav_item(app, y, 2, "Range", "Range")

    y += 9
    _group_label(c, y, "TOOLS")
    y += 14
    for mode_id, display, icon_kind in (
        (6, "Bag", "Bag"),
        (7, "Fit", "Fit"),
        (8, "Lab", "Lab"),
        (10, "Setup", None),
    ):
        y = _nav_item(app, y, mode_id, display, icon_kind)

    # Persistent reopen handle remains visually separate from nav groups.
    if getattr(app, "sidebar_collapsed", False):
        app.sidebar_toggle_rect = (rw - 24, 54, rw - 3, 88)
        app.design_sidebar_toggle_rect = (rw - 31, 50, rw, 94)
        c.create_rectangle(rw - 29, 55, rw - 2, 89,
                           fill=_mix(theme.SURFACE_2, BLUE, .07), outline="")
        v7._draw_chevron(c, rw - 15, 72, "right")


def paint_sidebar(app, w, h):
    return v11.paint_sidebar(app, w, h)


def paint_top_header(app, w, h, offset_x=0):
    return v11.paint_top_header(app, w, h, offset_x=offset_x)
