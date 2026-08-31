"""Twelfth-pass shell: strong section ribbons for the left navigation.

The underlying destinations, icons, sidebar, header branding, and hit targets
remain unchanged. This pass makes Session / Practice / Tools read as true
sections rather than small captions floating between nav items.
"""

import shell_redesign_v10 as v10
import shell_redesign_v11 as v11
import shell_redesign_v7 as v7
import theme


SECTION_H = 22
SECTION_GAP_BEFORE = 30
SECTION_GAP_AFTER = 8


def _section_band(c, y, text):
    """Full-width, consistent blue ribbon for a navigation section."""
    rw = theme.RAIL_W
    c.create_rectangle(0, y, rw, y + SECTION_H, fill=theme.ACCENT, outline="")
    c.create_text(
        rw / 2,
        y + SECTION_H / 2,
        text=text,
        fill=theme.TEXT,
        font=(theme.ui_font(), 8, "bold"),
        anchor="center",
    )
    return y + SECTION_H


def paint_nav(app, h):
    c = app.canvas
    rw = theme.RAIL_W
    shell_bg = v10._mix(theme.RAIL, theme.BG, .42)

    c.create_rectangle(0, 0, rw, h, fill=shell_bg, outline="")
    c.create_line(rw - 1, 0, rw - 1, h,
                  fill=v10._mix(theme.HAIRLINE, theme.BG, .46))

    app.mode_pill_rects = {}
    app.design_mode_rects = {}

    # SESSION
    y = 62
    y = _section_band(c, y, "SESSION") + SECTION_GAP_AFTER
    for mode_id, display, icon_kind in (
        (9, "Shot", "Overview"),
        (1, "Club", None),
        (3, "Dispersion", "Disp"),
        (4, "Table", "Table"),
        (5, "Numbers", "Nums"),
    ):
        y = v10._nav_item(app, y, mode_id, display, icon_kind)

    # PRACTICE — deliberate whitespace before the next ribbon so the previous
    # section visibly ends before the next one begins.
    y += SECTION_GAP_BEFORE
    y = _section_band(c, y, "PRACTICE") + SECTION_GAP_AFTER
    y = v10._nav_item(app, y, 2, "Range", "Range")

    # TOOLS
    y += SECTION_GAP_BEFORE
    y = _section_band(c, y, "TOOLS") + SECTION_GAP_AFTER
    for mode_id, display, icon_kind in (
        (6, "Bag", "Bag"),
        (7, "Fit", "Fit"),
        (8, "Lab", "Lab"),
        (10, "Setup", None),
    ):
        y = v10._nav_item(app, y, mode_id, display, icon_kind)

    # Preserve the existing reliable Recent Shots reopen affordance.
    if getattr(app, "sidebar_collapsed", False):
        app.sidebar_toggle_rect = (rw - 24, 57, rw - 3, 84)
        app.design_sidebar_toggle_rect = (rw - 31, 53, rw, 90)
        c.create_rectangle(
            rw - 30, 55, rw - 2, 89,
            fill=v10._mix(theme.SURFACE_2, theme.ACCENT, .07), outline=""
        )
        v7._draw_chevron(c, rw - 15, 72, "right")


def paint_sidebar(app, w, h):
    return v11.paint_sidebar(app, w, h)


def paint_top_header(app, w, h, offset_x=0):
    return v11.paint_top_header(app, w, h, offset_x=offset_x)
