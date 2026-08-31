"""Central design tokens for Shanktuary Performance Studio.

Why this exists
---------------
The desktop UI grew to 195 distinct hex literals across ~734 usages. Colour
stopped carrying meaning, so this module is the single source of truth.

Design-pass rules:

* ONE cool neutral ramp (BG -> SURFACE -> HAIRLINE -> TEXT*) builds structure.
* ONE electric-blue brand scale marks identity, active state, and current data.
* SEMANTIC colours (GOOD / WARN / DANGER) are reserved for meaning and must
  never be used decoratively.
* Dense data surfaces stay mostly neutral; colour should explain, not compete.
"""

# --- neutral ramp ---------------------------------------------------------
BG        = "#0B0F16"   # app background / graphite
RAIL      = "#0E1420"   # nav rail / ink
SURFACE   = "#111923"   # cards / panels
SURFACE_2 = "#182334"   # hover, selected row, raised surface
HAIRLINE  = "#253247"   # 1px separators

TEXT      = "#F3F6FA"   # primary values / headings
TEXT_2    = "#A6B0BE"   # labels, secondary copy / silver
TEXT_3    = "#657286"   # units, captions, disabled

# --- brand accent: electric blue scale -----------------------------------
ACCENT_DEEP = "#112A4E"  # selected backgrounds / pressed states
ACCENT      = "#1E6CFF"  # primary fills / active nav / current shot
ACCENT_LINE = "#40A3FF"  # strokes, plot highlights, icon detail
ACCENT_TEXT = "#78BAFF"  # readable blue text on dark surfaces

# --- semantic -------------------------------------------------------------
GOOD   = "#39A879"   # positive / healthy / consistent; deliberately muted
WARN   = "#F47A32"   # orange: estimates, attention, moderate miss
DANGER = "#E34A4A"   # red: bad outcome, error, extreme miss
GOLD   = "#C89A4A"   # restrained secondary emphasis / score or benchmark
GUIDE  = "#34445B"   # dashed reference/target lines

# Values the Nova cannot measure render in TEXT_3 with a "--" placeholder.
# See compute_smash_confidence(): a clamped OpenGolfCoach estimate carries no
# information, so it must not be styled like a measurement.
MUTED = TEXT_3

# --- layout ---------------------------------------------------------------
RAIL_W = 64          # left icon rail, always visible


# --- typography -----------------------------------------------------------
# Tk resolves unknown families silently, and "Helvetica" is NOT installed on
# most Linux systems -- it falls back to Nimbus Sans, a narrow URW clone that
# reads as monospace-ish at small sizes. Resolve a real UI face once, at
# import, and use it everywhere.
def _resolve_ui_font():
    try:
        import tkinter.font as tkfont
        fams = set(tkfont.families())
    except Exception:
        return "Helvetica"
    for cand in ("Inter", "Noto Sans", "DejaVu Sans", "Liberation Sans",
                 "Cantarell", "Segoe UI", "Helvetica Neue", "Arial"):
        if cand in fams:
            return cand
    return "Helvetica"


_UI_FONT = None


def ui_font():
    """Family name for all UI text. Resolved lazily -- needs a live Tk root."""
    global _UI_FONT
    if _UI_FONT is None:
        _UI_FONT = _resolve_ui_font()
    return _UI_FONT


NAV_ITEM_H = 56      # per nav entry
CORNER = 10          # standard corner radius

# view_mode -> (rail label, tooltip).
# NOTE: mode 0 is the floor divot projector (entered via Tools, not the rail)
# and mode 5 is Big Numbers. Overview is mode 9 to avoid colliding with either.
NAV_ITEMS = [
    (9, "Overview", "Shot summary and session trends"),
    (1, "Quad",     "Four-panel club and ball geometry"),
    (2, "Range",    "3D driving range"),
    (3, "Disp",     "Dispersion and covariance"),
    (4, "Table",    "Shot table"),
    (5, "Nums",     "Big numbers"),
    (6, "Bag",      "My Bag and club specs"),
    (7, "Fit",      "Club fitting comparison"),
    (8, "Lab",      "Swing lab / pressure"),
]
