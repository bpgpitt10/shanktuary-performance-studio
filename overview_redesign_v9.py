"""Ninth-pass Shot view: dynamic movement geometry and clearer session review."""

from __future__ import annotations

import math
import statistics

import overview_redesign_v5 as v5
import overview_redesign_v7 as v7
import overview_redesign_v8 as v8
import theme

BLUE = v7.BLUE
BLUE_LINE = v7.BLUE_LINE
BLUE_TEXT = v7.BLUE_TEXT
ORANGE = v7.ORANGE
GOLD = v7.GOLD
GOOD = v7.GOOD

_values = v7._values
_movement = v7._movement
_side = v7._side
_ui_font = v7._ui_font
_mix = v7._mix
_club_speed = v7._club_speed
_sparkline = v7._sparkline
_draw_pair_metric = v7._draw_pair_metric

SOFT_LINE = v7.SOFT_LINE
GRID_LINE = v7.GRID_LINE
SESSION_DOT = v7.SESSION_DOT
SECTION_TEXT = v7.SECTION_TEXT
SHAPE_TEXT = v7.SHAPE_TEXT
NEUTRAL_POINT = v7.NEUTRAL_POINT

CONFIDENCE = v8.CONFIDENCE
CONF_RADIUS = v8.CONF_RADIUS


def _depth_background(app, x0, y0, x1, y1):
    return v8._depth_background(app, x0, y0, x1, y1)


def _ribbon_surface(app, x0, y0, x1, y1):
    return v8._ribbon_surface(app, x0, y0, x1, y1)


def _session_surface(app, x0, y0, x1, y1):
    """A distinct review surface with a pronounced top tonal fade, not a rule."""
    img = v8._material_image(
        app, "overview_v9_session", x1 - x0, y1 - y0,
        top="#10243A", bottom="#05080D",
        left="#0A1826", right="#0A1018",
        mottle=.070, fibers=.026, grain=.018, seed=131,
    )
    c = app.canvas
    c.create_image(x0, y0, image=img, anchor="nw")

    # Reinforce only the top 58px so the eye reads a new review mode without
    # introducing another decorative line that competes with shot movement.
    band_h = min(58, max(1, y1 - y0))
    for i in range(band_h):
        t = i / max(1, band_h - 1)
        col = _mix("#122A43", "#09131E", t)
        c.create_line(x0, y0 + i, x1, y0 + i, fill=col)


def _draw_dispersion(app, x0, y0, x1, y1, shots):
    c = app.canvas
    club = (app.current_shot or {}).get("club") or app.current_club
    v7._section_title(c, x0, y0, "Dispersion", f"{club} · carry landing pattern")

    points = [(_values(s), s) for s in shots]
    points = [(vv, ss) for vv, ss in points if vv["carry"] > 0]
    if not points:
        return

    left, right = x0 + 46, x1 - 18
    top, bottom = y0 + 64, y1 - 48
    carries = [vv["carry"] for vv, _ in points]
    offs = [vv["offline"] for vv, _ in points]
    mc, mo = statistics.mean(carries), statistics.mean(offs)
    sc = statistics.pstdev(carries) if len(carries) > 1 else 2.5
    so = statistics.pstdev(offs) if len(offs) > 1 else 2.0

    carry_half = CONF_RADIUS * max(1.5, sc)
    raw_min = min(min(carries), mc - carry_half)
    raw_max = max(max(carries), mc + carry_half)
    raw_span = max(8.0, raw_max - raw_min)
    pad = raw_span * .075
    cmin, cmax = raw_min - pad, raw_max + pad

    lateral_extent = max(
        5.0,
        max(abs(v) for v in offs),
        abs(mo) + CONF_RADIUS * max(1.0, so),
    )
    omax = lateral_extent * 1.07
    pw, ph = right - left, bottom - top

    def sx(off):
        return left + (off + omax) / (2 * omax) * pw

    def sy(car):
        return bottom - (car - cmin) / max(.01, cmax - cmin) * ph

    tx = sx(0)
    for frac in (.34, .67):
        gy = top + ph * frac
        val = cmax - (cmax - cmin) * frac
        c.create_line(left, gy, right, gy, fill=GRID_LINE, dash=(2, 6))
        c.create_text(left - 9, gy, text=f"{val:.0f}", fill=theme.TEXT_3,
                      font=(_ui_font(), 8), anchor="e")
    c.create_line(tx, top, tx, bottom, fill=GRID_LINE, dash=(4, 6))

    ex0 = sx(mo - CONF_RADIUS * max(1.0, so))
    ex1 = sx(mo + CONF_RADIUS * max(1.0, so))
    ey0 = sy(mc + carry_half)
    ey1 = sy(mc - carry_half)
    ellipse_col = _mix(BLUE_LINE, theme.BG, .34)
    c.create_oval(ex0, ey0, ex1, ey1, outline=ellipse_col, width=2)
    c.create_text(ex1 - 7, ey0 + 8, text="90% confidence",
                  fill=_mix(BLUE_TEXT, theme.BG, .18),
                  font=(_ui_font(), 9, "bold"), anchor="ne")

    for vv, shot in points:
        px, py = sx(vv["offline"]), sy(vv["carry"])
        if shot is app.current_shot:
            c.create_oval(px - 10, py - 10, px + 10, py + 10,
                          fill=ORANGE, outline="")
        else:
            c.create_oval(px - 4, py - 4, px + 4, py + 4,
                          fill=SESSION_DOT, outline="")

    c.create_text(left, bottom + 15, text=f"{omax:.0f}L", fill=theme.TEXT_3,
                  font=(_ui_font(), 9), anchor="n")
    c.create_text(tx, bottom + 15, text="TARGET", fill=theme.TEXT_3,
                  font=(_ui_font(), 9, "bold"), anchor="n")
    c.create_text(right, bottom + 15, text=f"{omax:.0f}R", fill=theme.TEXT_3,
                  font=(_ui_font(), 9), anchor="n")

    c.create_oval(x0 + 2, y1 - 20, x0 + 14, y1 - 8, fill=ORANGE, outline="")
    c.create_text(x0 + 20, y1 - 14, text="Current shot", fill=theme.TEXT_2,
                  font=(_ui_font(), 10), anchor="w")
    c.create_oval(x0 + 124, y1 - 18, x0 + 130, y1 - 12,
                  fill=SESSION_DOT, outline="")
    c.create_text(x0 + 136, y1 - 15, text=f"Session ({len(points)})",
                  fill=theme.TEXT_2, font=(_ui_font(), 10), anchor="w")


def _draw_shape(app, x0, y0, x1, y1, v, shots):
    c = app.canvas
    v7._section_title(c, x0, y0, "Shot Shape")
    start, move = _movement(v)

    direction = "Right → Left" if move < -1.5 else (
        "Left → Right" if move > 1.5 else "Minimal curve")

    # Shape and direction share a true vertical center rather than two nearby baselines.
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
    c.create_line(tx, ay - 42, tx, ay + 48, fill=SOFT_LINE, dash=(3, 6))

    # Stop the arrow just before the finish ball so its point stays visible.
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

    # Labels follow the actual marker positions. When markers are close, fan
    # labels outward so a near-straight shot remains readable.
    def clamp(vv, lo, hi):
        return max(lo, min(hi, vv))

    start_lx, finish_lx = sx, ex
    if abs(sx - ex) < 96:
        if sx <= ex:
            start_lx = sx - 44
            finish_lx = ex + 44
        else:
            start_lx = sx + 44
            finish_lx = ex - 44
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
    c.create_text(tx, fact_y + 48, text="TARGET", fill=theme.TEXT_3,
                  font=(_ui_font(), 9, "bold"), anchor="n")

    mix_y = y1 - 86
    c.create_line(x0, mix_y - 14, x1, mix_y - 14, fill=SOFT_LINE)
    v7._draw_shape_mix(c, x0, mix_y, x1, shots)


def _draw_delivery_panel(app, x0, y0, x1, y1, v):
    """One cohesive cause panel: strike first, then path/face, no divider."""
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

    path_y = y0 + hh * .55
    c.create_text(x0, path_y, text="Path & Face", fill=theme.TEXT_2,
                  font=(_ui_font(), 11, "bold"), anchor="nw")

    table_w = w * .40
    rows = [
        ("Path", f"{abs(v['path']):.1f}° {'in→out' if v['path'] >= 0 else 'out→in'}"),
        ("Face / Path", f"{abs(v['face_path']):.1f}° {'open' if v['face_path'] >= 0 else 'closed'}"),
        ("Face / Target", f"{abs(v['face_target']):.1f}° {'open' if v['face_target'] >= 0 else 'closed'}"),
        ("Spin Axis", f"{abs(v['axis']):.1f}° {'R' if v['axis'] > 0 else 'L'}"),
    ]
    yy = path_y + 31
    for label, value in rows:
        c.create_text(x0, yy, text=label, fill=theme.TEXT_2,
                      font=(_ui_font(), 9), anchor="nw")
        c.create_text(x0 + table_w * .45, yy - 1, text=value, fill=SECTION_TEXT,
                      font=(_ui_font(), 10, "bold"), anchor="nw")
        yy += 24

    gx0, gx1 = x0 + table_w + 2, x1 - 4
    cx = (gx0 + gx1) / 2
    cy = path_y + min(92, (y1 - path_y) * .53)
    length = min(58, max(36, (y1 - path_y) * .28))
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


def _sd(vals, unit=""):
    if len(vals) <= 1:
        return "SD —"
    val = statistics.pstdev(vals)
    if unit == "rpm":
        return f"SD {val:.0f} {unit}"
    return f"SD {val:.1f}{(' ' + unit) if unit else ''}"


def _draw_session_bottom(app, x0, y0, x1, y1, shots):
    c = app.canvas
    vals = [_values(s) for s in shots]
    if not vals:
        return

    club = (app.current_shot or {}).get("club") or app.current_club
    speeds = [_club_speed(s) for s in shots]
    avg = lambda key: statistics.mean(v[key] for v in vals)
    avg_club = statistics.mean(speeds) if speeds else 0.0

    total_w = x1 - x0
    summary_w = total_w * .37
    divider = x0 + summary_w

    # Mixed-color header: club is the same blue used in the current-shot ribbon.
    title_id = c.create_text(x0, y0 + 15, text="Session ·", fill=SECTION_TEXT,
                             font=(_ui_font(), 14, "bold"), anchor="nw")
    bb = c.bbox(title_id)
    club_x = (bb[2] + 7) if bb else x0 + 72
    c.create_text(club_x, y0 + 15, text=club, fill=BLUE_TEXT,
                  font=(_ui_font(), 14, "bold"), anchor="nw")
    c.create_text(divider - 16, y0 + 18, text=f"{len(vals)} shots",
                  fill=theme.TEXT_2, font=(_ui_font(), 10, "bold"), anchor="ne")

    summary = [
        ("Carry", f"{avg('carry'):.1f} yds"),
        ("Total", f"{avg('total'):.1f} yds"),
        ("Ball", f"{avg('ball'):.1f} mph"),
        ("Club", f"{avg_club:.1f} mph"),
        ("VLA", f"{avg('launch'):.1f}°"),
        ("Spin", f"{avg('spin'):.0f} rpm"),
        ("Offline", f"{_side(avg('offline'))} yds"),
        ("Smash", f"{avg('smash'):.2f}"),
    ]
    inner_w = summary_w - 22
    cell_w = inner_w / 4
    for i, (label, value) in enumerate(summary):
        col, row = i % 4, i // 4
        xx = x0 + col * cell_w
        yy = y0 + 59 + row * 43
        c.create_text(xx, yy, text=label, fill=theme.TEXT_2,
                      font=(_ui_font(), 9, "bold"), anchor="w")
        c.create_text(xx + cell_w - 8, yy, text=value, fill=SECTION_TEXT,
                      font=(_ui_font(), 10, "bold"), anchor="e")

    c.create_line(divider + 2, y0 + 12, divider + 2, y1 - 8, fill=SOFT_LINE)

    recent = vals[-min(16, len(vals)):]
    carries = [v["carry"] for v in recent]
    balls = [v["ball"] for v in recent]
    spins = [v["spin"] for v in recent]
    offlines = [v["offline"] for v in recent]
    starts = [_movement(v)[0] for v in recent]
    moves = [_movement(v)[1] for v in recent]

    trend_x0 = divider + 30
    c.create_text(trend_x0, y0 + 15, text="Session Trends", fill=SECTION_TEXT,
                  font=(_ui_font(), 14, "bold"), anchor="nw")
    c.create_text(x1, y0 + 18, text=f"Last {min(16, len(vals))} shots",
                  fill=theme.TEXT_2, font=(_ui_font(), 10, "bold"), anchor="ne")

    rows_left = [
        ("Carry", f"Avg {statistics.mean(carries):.1f} yds", _sd(carries, "yds"), carries, BLUE_LINE),
        ("Spin", f"Avg {statistics.mean(spins):.0f} rpm", _sd(spins, "rpm"), spins, GOLD),
        ("Offline", f"Avg {_side(statistics.mean(offlines))} yds", _sd(offlines, "yds"), offlines, ORANGE),
    ]
    rows_right = [
        ("Start Line", f"Avg {_side(statistics.mean(starts))} yds", _sd(starts, "yds"), starts, BLUE_TEXT),
        ("Curve Movement",
         f"Avg {abs(statistics.mean(moves)):.1f}{'L' if statistics.mean(moves) < 0 else 'R'} yds",
         _sd(moves, "yds"), moves, ORANGE),
        ("Ball Speed", f"Avg {statistics.mean(balls):.1f} mph", _sd(balls, "mph"), balls, GOOD),
    ]

    gap = 28
    trend_w = x1 - trend_x0
    col_w = (trend_w - gap) / 2

    def draw_rows(rows, bx0, bx1):
        yy = y0 + 53
        for label, avg_text, detail, arr, color in rows:
            c.create_text(bx0, yy, text=label, fill=theme.TEXT_2,
                          font=(_ui_font(), 10, "bold"), anchor="nw")
            c.create_text(bx0, yy + 21, text=avg_text, fill=SECTION_TEXT,
                          font=(_ui_font(), 12, "bold"), anchor="nw")
            c.create_text(bx0 + 125, yy + 23, text=detail, fill=theme.TEXT_3,
                          font=(_ui_font(), 9), anchor="nw")
            _sparkline(c, bx0 + col_w * .62, yy + 22, bx1 - 4, arr, color)
            yy += 54

    draw_rows(rows_left, trend_x0, trend_x0 + col_w)
    draw_rows(rows_right, trend_x0 + col_w + gap, x1)


def _fmt_hla(hla):
    if abs(hla) < .05:
        return "0.0°"
    return f"{abs(hla):.1f}° {'R' if hla > 0 else 'L'}"


def draw_overview(app, avail_w, h, carry, total, ball_speed, club_speed, smash,
                  launch, spin, apex, offline, descent, hang_time, club_path,
                  face_to_path, spin_axis, face_to_target=0.0, shot_name="",
                  smash_clamped=False, offset_x=0, top_bar_h=52):
    c = app.canvas
    _depth_background(app, offset_x, top_bar_h, offset_x + avail_w, h)

    app.overview_viewall_rect = None
    app.overview_prev_rect = None
    app.overview_next_rect = None
    app.overview_bar_rects = []

    shots_all = list(app.session_shots)
    shots = v7._club_shots(app)
    v = _values(app.current_shot)
    v.update({
        "carry": carry, "total": total, "ball": ball_speed, "smash": smash,
        "launch": launch, "spin": spin, "apex": apex, "offline": offline,
        "descent": descent, "hang": hang_time, "path": club_path,
        "face_path": face_to_path, "axis": spin_axis,
        "face_target": face_to_target, "shape": shot_name or v["shape"],
    })

    margin = max(18, int(avail_w * .015))
    gap = max(20, int(avail_w * .012))
    x0, x1 = offset_x + margin, offset_x + avail_w - margin
    y0 = top_bar_h + 14
    usable_h = h - y0 - 16

    top_h = max(148, min(164, int(usable_h * .19)))
    _ribbon_surface(app, x0, y0, x1, y0 + top_h)
    c.create_line(x0, y0 + top_h, x1, y0 + top_h, fill=SOFT_LINE)
    c.create_rectangle(x0, y0, x0 + 4, y0 + top_h, fill=BLUE, outline="")

    n = len(shots_all)
    idx = app.selected_shot_index + 1 if app.selected_shot_index is not None else n
    identity_w = max(270, min(330, (x1 - x0) * .205))
    ix = x0 + 24
    club = (app.current_shot or {}).get("club") or app.current_club
    c.create_text(ix, y0 + 22, text=f"Shot {idx}", fill=theme.TEXT_2,
                  font=(_ui_font(), 12, "bold"), anchor="nw")
    c.create_text(ix + 78, y0 + 19, text=club, fill=BLUE_TEXT,
                  font=(_ui_font(), 16, "bold"), anchor="nw")
    c.create_text(ix, y0 + 58, text=(shot_name or "Straight"), fill=SECTION_TEXT,
                  font=(_ui_font(), 28, "bold"), anchor="nw")

    mx0 = x0 + identity_w
    step = (x1 - mx0) / 6
    for i in range(1, 6):
        xx = mx0 + i * step
        c.create_line(xx, y0 + 24, xx, y0 + top_h - 24, fill=SOFT_LINE)

    _draw_pair_metric(c, mx0 + 16, y0 + 22, mx0 + step,
                      "Carry", f"{carry:.1f}", "yds",
                      "Total", f"{total:.1f}", "yds")
    _draw_pair_metric(c, mx0 + step + 16, y0 + 22, mx0 + step * 2,
                      "Ball Speed", f"{ball_speed:.1f}", "mph",
                      "Club", f"{club_speed:.1f}", "mph")
    _draw_pair_metric(c, mx0 + step * 2 + 16, y0 + 22, mx0 + step * 3,
                      "VLA", f"{launch:.1f}°", "",
                      "HLA", _fmt_hla(v.get("hlaunch", 0.0)), "")
    v5._draw_single_metric(c, mx0 + step * 3 + 16, y0 + 22,
                           "Spin Rate", f"{spin:.0f}", "rpm")
    v5._draw_single_metric(c, mx0 + step * 4 + 16, y0 + 22,
                           "Apex", f"{apex * 3:.0f}", "ft")
    v5._draw_single_metric(c, mx0 + step * 5 + 16, y0 + 22,
                           "Offline", _side(offline), "yds")

    main_y0 = y0 + top_h + gap
    bottom_h = max(205, min(232, int(usable_h * .255)))
    main_y1 = h - 16 - bottom_h - gap
    main_h = max(350, main_y1 - main_y0)
    main_y1 = main_y0 + main_h

    total_w = x1 - x0
    lw = total_w * .40
    cw = total_w * .29
    dx0, dx1 = x0, x0 + lw
    sx0, sx1 = dx1 + gap, dx1 + gap + cw
    rx0, rx1 = sx1 + gap, x1

    c.create_line(dx1 + gap / 2, main_y0 + 4, dx1 + gap / 2,
                  main_y1 - 4, fill=SOFT_LINE)
    c.create_line(sx1 + gap / 2, main_y0 + 4, sx1 + gap / 2,
                  main_y1 - 4, fill=SOFT_LINE)

    _draw_dispersion(app, dx0, main_y0, dx1, main_y1, shots)
    _draw_shape(app, sx0, main_y0, sx1, main_y1, v, shots)
    _draw_delivery_panel(app, rx0, main_y0, rx1, main_y1, v)

    by0, by1 = main_y1 + gap, h - 16
    if by1 - by0 >= 170:
        _session_surface(app, x0, by0 - 7, x1, by1)
        _draw_session_bottom(app, x0, by0 - 7, x1, by1, shots)
