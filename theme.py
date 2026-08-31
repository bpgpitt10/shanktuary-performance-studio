"""Legacy/shared production tokens for Shanktuary Performance Studio.

IMPORTANT FOR DESIGN WORK
-------------------------
The accepted desktop redesign on `feature/shot-polish-clean` uses the premium
navy + teal + antique-gold system documented in `DESIGN_BASELINE.md`.

This module still contains the older production electric-blue token values
because changing them globally would also affect legacy desktop/browser
surfaces that have not been migrated in the same way. The design launcher
therefore applies the accepted palette through page-local wrappers such as:

- `overview_redesign_v14.py` / `overview_redesign_v15.py`
- `shell_redesign_v13.py` / `shell_redesign_v14.py`
- `club_redesign_v3.py`
- `table_redesign_v2.py`
- `numbers_redesign_v2.py`
- `remaining_pages_palette_v1.py`

Do NOT treat the electric-blue values below as the current brand direction when
adding or restyling desktop UI. Start with `DESIGN_BASELINE.md` instead.

The shared tokens remain here so legacy code continues to render safely until a
deliberate full-app migration consolidates everything into one global theme.
"""

# --- legacy neutral ramp --------------------------------------------------
BG        = "#0B0F16"   # legacy app background / graphite
RAIL      = "#0E1420"   # legacy nav rail / ink
SURFACE   = "#111923"   # legacy cards / panels
SURFACE_2 = "#182334"   # legacy hover, selected row, raised surface
HAIRLINE  = "#253247"   # legacy 1px separators

TEXT      = "#F3F6FA"   # primary values / headings
TEXT_2    = "#A6B0BE"   # labels, secondary copy / silver
TEXT_3    = "#657286"   # units, captions, disabled

# --- LEGACY accent scale --------------------------------------------------
# The accepted desktop redesign does NOT use electric blue as its brand accent.
# See DESIGN_BASELINE.md for the current gold/teal system.
ACCENT_DEEP = "#112A4E"
ACCENT      = "#1E6CFF"
ACCENT_LINE = "#40A3FF"
ACCENT_TEXT = "#78BAFF"

# --- semantic / legacy compatibility -------------------------------------
GOOD   = "#39A879"   # positive / healthy / ready state
WARN   = "#F47A32"   # legacy warning color; redesign usually maps emphasis to gold
DANGER = "#E34A4A"   # bad outcome / error / extreme miss
GOLD   = "#C89A4A"   # legacy gold token; redesign uses #D4A24F
GUIDE  = "#34445B"   # legacy dashed reference/target lines

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

# Legacy production navigation labels. The active redesign hierarchy lives in
# shell_redesign_v13.py and is documented in DESIGN_BASELINE.md.
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
