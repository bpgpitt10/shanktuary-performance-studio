"""Central design tokens for Shanktuary Performance Studio.

Why this exists
---------------
The desktop UI grew to 195 distinct hex literals across ~734 usages. Colour
stopped carrying meaning, so this module is the single source of truth.

Design-pass rules:

* ONE deep navy ramp (BG -> SURFACE -> HAIRLINE -> TEXT*) builds structure.
* WARM GOLD / BRONZE is the primary Shanktuary brand accent.
* MUTED TEAL is the secondary data accent for charts and analytical geometry.
* SEMANTIC colours (GOOD / WARN / DANGER) are reserved for meaning.
* Dense data surfaces stay mostly neutral; colour should explain, not compete.
"""

# --- neutral ramp ---------------------------------------------------------
BG        = "#08131F"   # main background / ink navy
RAIL      = "#0C1928"   # navigation rail / deep navy
SURFACE   = "#111F2F"   # cards / panels / containers
SURFACE_2 = "#192B3E"   # hover, selected row, raised surface
HAIRLINE  = "#2A3B4D"   # 1px separators

TEXT      = "#F1F3F2"   # primary values / headings
TEXT_2    = "#AEB8C2"   # labels, secondary copy / silver
TEXT_3    = "#71808E"   # units, captions, disabled

# --- primary brand accent: antique gold / bronze -------------------------
ACCENT_DEEP = "#3A2C1B"  # selected backgrounds / pressed states
ACCENT      = "#C99A4A"  # primary fills / active nav / current shot
ACCENT_LINE = "#E0B866"  # gold strokes, active outlines, icon detail
ACCENT_TEXT = "#E6C477"  # readable champagne-gold text on dark surfaces

# --- secondary data accent: muted teal -----------------------------------
DATA       = "#2E8290"   # secondary analytical accent
DATA_LINE  = "#62A9B3"   # chart lines, trajectories, analytical geometry
DATA_TEXT  = "#82BDC5"   # readable teal text on dark surfaces
BRONZE     = "#9B6E32"   # secondary gold / dark metallic accent

# --- semantic -------------------------------------------------------------
GOOD   = "#4B9A72"   # positive / healthy / consistent; deliberately muted
WARN   = "#B8893D"   # burnished amber: caution / attention only
DANGER = "#B94B43"   # brick red: bad outcome / error / extreme miss
GOLD   = ACCENT       # compatibility alias for older design helpers
GUIDE  = "#31495A"   # dashed reference/target lines

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
