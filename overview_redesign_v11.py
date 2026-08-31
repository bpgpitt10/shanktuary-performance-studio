"""Eleventh-pass Shot view: simplify target guide and use spare delivery space for interpretation."""

import math

import overview_redesign_v7 as v7
import overview_redesign_v9 as v9
import overview_redesign_v10 as v10
import theme

BLUE_LINE = v7.BLUE_LINE
BLUE_TEXT = v7.BLUE_TEXT
ORANGE = v7.ORANGE
GOOD = v7.GOOD
_values = v7._values
_movement = v7._movement
_side = v7._side
_ui_font = v7._ui_font
_mix = v7._mix
SOFT_LINE = v7.SOFT_LINE
GRID_LINE = v7.GRID_LINE
SECTION_TEXT = v7.SECTION_TEXT
SHAPE_TEXT = v7.SHAPE_TEXT
NEUTRAL_POINT = v7.NEUTRAL_POINT


def _draw_shape(app, x0, y0, x1, y1, v, shots):
    c = app.canvas
    v7._section_title(c, x0, y0, "Shot Shape")
    start, move = _movement(v)

    direction = "Right → Left" if move < -1.5 else (
        "Left → Right" if move > 1.5 else "Minimal curve")
    shape_y = y0 + 54
    shape_id = c.create_text(x0, shape_y, text=v["shape"], fill=SHAPE_TEXT,
                             font=(_ui_font(), 18, "bold"), anchor="w")
    bb = c.bbox(shape_id)
    direction_x = (bb[2] + 12) if bb else x0 + 120
    c.create_text(direction_x, shape_y, text=f"·  {direction}", fill=ORANGE,
                  font=(_ui_font(), 13, "bold"), anchor="w")

    hero_y = y0 + 96
    c.create_text(x0, hero_y, text="Movement", fill=theme.TEXT_2,
                  font=(_ui_font(), 11, "bold"), anchor="nw")
    move_dir = "R" if move > 0.12 else ("L" if move < -0.12 else "")
    c.create_text(x0, hero_y + 23, text=f"{abs(move):.1f} yds {move_dir}".strip(),
                  fill=ORANGE, font=(_ui_font(), 28, "bold"), anchor="nw")

    ax0, ax1 = x0 + 14, x1 - 14
    ay = y0 + min(216, (y1 - y0) * .49)
    scale = max(5.0, abs(start) * 1.35, abs(v["offline"]) * 1.35)
    mid = (ax0 + ax1) / 2
    span = (ax1 - ax0) / 2

    def px(val):
        return mid + val / scale * span

    sx, ex, tx = px(start), px(v["offline"]), px(0.0)
    c.create_line(ax0, ay, ax1, ay, fill=theme.GUIDE, width=1)
    # Target is now communicated by the stronger center guide alone.
    target_col = _mix(theme.GUIDE, BLUE_TEXT, .28)
    c.create_line(tx, ay - 54, tx, ay + 55, fill=target_col,
                  width=2, dash=(5, 5))

    delta = ex - sx
    if abs(delta) > 18:
        direction_sign = 1 if delta > 0 else -1
        arrow_end = ex - direction_sign * 15
        c.create_line(sx, ay, arrow_end, ay, fill=BLUE_LINE, width=4,
                      arrow="last", arrowshape=(13, 15, 6))
    else:
        c.create_line(sx, ay, ex, ay, fill=BLUE_LINE, width=4)

    c.create_oval(sx - 8, ay - 8, sx + 8, ay + 8,
                  fill=theme.BG, outline=BLUE_LINE, width=2)
    c.create_oval(ex - 9, ay - 9, ex + 9, ay + 9,
                  fill=NEUTRAL_POINT, outline=theme.TEXT_2, width=1)

    def clamp(vv, lo, hi):
        return max(lo, min(hi, vv))

    start_lx, finish_lx = sx, ex
    if abs(sx - ex) < 96:
        if sx <= ex:
            start_lx, finish_lx = sx - 44, ex + 44
        else:
            start_lx, finish_lx = sx + 44, ex - 44
    start_lx = clamp(start_lx, ax0 + 40, ax1 - 40)
    finish_lx = clamp(finish_lx, ax0 + 40, ax1 - 40)

    fact_y = ay + 17
    c.create_text(start_lx, fact_y, text="START", fill=theme.TEXT_3,
                  font=(_ui_font(), 9, "bold"), anchor="n")
    c.create_text(start_lx, fact_y + 18, text=f"{_side(start)} yds", fill=BLUE_TEXT,
                  font=(_ui_font(), 11, "bold"), anchor="n")
    c.create_text(finish_lx, fact_y, text="FINISH", fill=theme.TEXT_3,
                  font=(_ui_font(), 9, "bold"), anchor="n")
    c.create_text(finish_lx, fact_y + 18, text=f"{_side(v['offline'])} yds",
                  fill=SECTION_TEXT, font=(_ui_font(), 11, "bold"), anchor="n")

    mix_y = y1 - 86
    c.create_line(x0, mix_y - 14, x1, mix_y - 14, fill=SOFT_LINE)
    v7._draw_shape_mix(c, x0, mix_y, x1, shots)


def _delivery_takeaway(v):
    path = float(v.get("path", 0.0))
    fp = float(v.get("face_path", 0.0))
    if path > 0.7:
        p = "In-to-out delivery"
    elif path < -0.7:
        p = "Out-to-in delivery"
    else:
        p = "Neutral path"

    if abs(fp) <= 0.6:
        f = "face nearly square to path"
    elif fp > 0:
        f = "face open to path"
    else:
        f = "face closed to path"
    return f"{p} · {f}"


def _draw_delivery_panel(app, x0, y0, x1, y1, v):
    """Cohesive cause panel with a compact interpretation layer."""
    c = app.canvas
    title_id = c.create_text(x0, y0, text="Club Delivery", fill=SECTION_TEXT,
                             font=(_ui_font(), 14, "bold"), anchor="nw")
    bb = c.bbox(title_id)
    tx = (bb[2] + 8) if bb else x0 + 92
    c.create_text(tx, y0 + 7, text="· Estimated", fill=ORANGE,
                  font=(_ui_font(), 11, "bold"), anchor="w")

    w, hh = x1 - x0, y1 - y0
    strike_y = y0 + 44
    c.create_text(x0, strike_y, text="Strike", fill=theme.TEXT_2,
                  font=(_ui_font(), 11, "bold"), anchor="nw")
    head, detail, _hcol = app.summarize_strike(app.current_shot)
    col = GOOD if ("center" in head.lower() or "pure" in head.lower()) else SECTION_TEXT
    c.create_text(x0, strike_y + 29, text=head, fill=col,
                  font=(_ui_font(), 15, "bold"), anchor="nw")
    c.create_text(x0, strike_y + 56, text=detail, fill=theme.TEXT_3,
                  font=(_ui_font(), 10), anchor="nw", width=max(110, int(w * .34)))

    face_cx = x0 + w * .73
    face_cy = strike_y + 60
    face_size = max(132, min(180, hh * .34, w * .56))
    app._draw_overview_face(face_cx, face_cy, face_size)

    path_y = y0 + hh * .52
    c.create_text(x0, path_y, text="Path & Face", fill=theme.TEXT_2,
                  font=(_ui_font(), 11, "bold"), anchor="nw")
    c.create_text(x0, path_y + 23, text=_delivery_takeaway(v),
                  fill=BLUE_TEXT, font=(_ui_font(), 9, "bold"), anchor="nw")

    table_w = w * .40
    rows = [
        ("Path", f"{abs(v['path']):.1f}° {'in→out' if v['path'] >= 0 else 'out→in'}"),
        ("Face / Path", f"{abs(v['face_path']):.1f}° {'open' if v['face_path'] >= 0 else 'closed'}"),
        ("Face / Target", f"{abs(v['face_target']):.1f}° {'open' if v['face_target'] >= 0 else 'closed'}"),
        ("Spin Axis", f"{abs(v['axis']):.1f}° {'R' if v['axis'] > 0 else 'L'}"),
    ]
    yy = path_y + 52
    for label, value in rows:
        c.create_text(x0, yy, text=label, fill=theme.TEXT_2,
                      font=(_ui_font(), 9), anchor="nw")
        c.create_text(x0 + table_w * .45, yy - 1, text=value, fill=SECTION_TEXT,
                      font=(_ui_font(), 10, "bold"), anchor="nw")
        yy += 24

    gx0, gx1 = x0 + table_w + 2, x1 - 4
    cx = (gx0 + gx1) / 2
    cy = path_y + min(112, (y1 - path_y) * .58)
    length = min(58, max(36, (y1 - path_y) * .27))
    mirror = -1 if getattr(app, "is_left_handed", False) else 1

    c.create_line(cx, cy + length + 12, cx, cy - length - 16,
                  fill=GRID_LINE, dash=(3, 5))
    c.create_text(cx, cy - length - 20, text="TARGET", fill=theme.TEXT_3,
                  font=(_ui_font(), 8, "bold"), anchor="s")

    path_deg = max(-12.0, min(12.0, v["path"]))
    dx = math.tan(math.radians(path_deg)) * length * mirror
    x_start, y_start = cx - dx, cy + length
    x_end, y_end = cx + dx, cy - length
    c.create_line(x_start, y_start, x_end, y_end, fill=BLUE_LINE, width=3,
                  arrow="last", arrowshape=(11, 13, 5))
    c.create_text(x_end + (8 if mirror > 0 else -8), y_end + 8, text="PATH",
                  fill=BLUE_TEXT, font=(_ui_font(), 8, "bold"),
                  anchor="w" if mirror > 0 else "e")

    face_deg = max(-16.0, min(16.0, v["face_target"])) * mirror
    theta = math.radians(face_deg)
    half = 28
    fx = math.cos(theta) * half
    fy = math.sin(theta) * half
    c.create_line(cx - fx, cy - fy, cx + fx, cy + fy, fill=ORANGE, width=4)
    c.create_oval(cx - 4, cy - 4, cx + 4, cy + 4,
                  fill=theme.TEXT_2, outline=theme.BG)
    c.create_text(cx + fx + 7, cy + fy, text="FACE", fill=ORANGE,
                  font=(_ui_font(), 8, "bold"), anchor="w")


def draw_overview(*args, **kwargs):
    # v10 keeps the accepted split session area; only replace the live-shot
    # helpers changed in this pass.
    v9._draw_shape = _draw_shape
    v9._draw_delivery_panel = _draw_delivery_panel
    return v10.draw_overview(*args, **kwargs)
