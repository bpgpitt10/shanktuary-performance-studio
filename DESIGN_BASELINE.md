# Shanktuary Design System & Baseline

This document is the design handoff for the current desktop redesign branch. Use it before changing visual styling so new work stays consistent with the accepted Shot / Club / Table / Numbers / shell direction.

## Current working branch

- App version in source: `v1.3.1`
- Design branch: `feature/shot-polish-clean`
- Production UI: `shanktuary_performance_studio.py`
- Design launcher / wiring: `design_overview_demo.py`
- Shared legacy tokens: `theme.py`
- Current shell: `shell_redesign_v14.py` + `shell_redesign_v13.py`
- Current Shot palette reference: `overview_redesign_v14.py` / `overview_redesign_v15.py`
- Remaining production-page palette adapter: `remaining_pages_palette_v1.py`

Important: `theme.py` still contains the older production electric-blue token set. On this branch, the accepted gold/teal redesign is intentionally applied in design wrappers/page-local palette passes. Do not assume the old electric-blue comments in `theme.py` describe the current visual direction.

## Brand direction

Shanktuary is now a premium golf-performance brand, not a church/sanctuary visual concept.

- Overall feel: premium, modern, technical, golf-performance oriented.
- Avoid: church architecture, crosses, heraldic/fantasy styling, electric blue, loud orange, excessive glow, and generic gamer/neon treatment.
- Brand artwork should use the approved PNG assets rather than rebuilding the logo with Tk text/shapes.
- Global header lockup asset: `assets/shanktuary_lockup.png`
- App / Dock icon asset: `assets/shanktuary_shield.png`
- Header implementation: `shell_redesign_v14.py`

## Accepted color system

### Core accents

| Role | Hex | Usage |
| --- | --- | --- |
| Antique Gold | `#D4A24F` | Primary emphasis, current shot, active selection, important metrics/actions |
| Light Gold | `#E3BC70` | Active icons, small highlights, readable gold detail |
| Core Teal | `#32979A` | Supporting analytical color / secondary brand accent |
| Teal Line | `#58B7B4` | Charts, geometry, paths, confidence ellipses, analytical strokes |
| Teal Text | `#78C4C1` | Readable teal labels / analytical takeaways |
| Soft Teal | `#698E96` | Secondary chart/data accents and restrained supporting detail |

### Core dark surfaces

| Role | Hex | Usage |
| --- | --- | --- |
| Main page navy | `#0A2029` | Default page material for legacy/restyled views |
| Rail navy | `#0B1B24` | Dark structural/nav surface |
| Surface | `#0D2731` | Cards/panels |
| Raised surface | `#15333D` | Selected/raised areas |
| Deep teal active | `#173B42` | Section bands / selected structural states |
| Hairline | `#2A4C55` | Dividers and quiet borders |
| Guide | `#456D76` | Target/reference guides |

Shot uses richer gradient/material variants of these values rather than a single flat fill; `overview_redesign_v14.py` is the visual reference for those surfaces.

### Text / semantic colors

| Role | Hex | Usage |
| --- | --- | --- |
| Primary text | `#F3F6FA` | Main values and headings |
| Secondary text | `#B3BEC2` | Labels and supporting copy |
| Muted text | `#70868C` | Units, captions, disabled/unavailable values |
| Success | `#39A879` | Genuine positive/ready/success state only |
| Danger | `#E34A4A` | Genuine error/danger/extreme negative state only |

## Color-role rules

1. **Gold = primary/current/active.** Use it for the current shot, active nav state, hero metric, selected row, important action, or intentional emphasis. Do not spray gold across generic chart series.
2. **Teal = analysis/data/geometry.** Paths, face/path diagrams, target geometry, confidence ellipses, supportive chart series, and analytical labels belong in teal.
3. **White = structure.** Section titles and primary values should usually be white/cool white rather than colored.
4. **Slate = context.** Units, subtitles, inactive controls, historical points, and supporting labels stay muted.
5. **Green and red are semantic only.** Green means success/ready/positive. Red means error/danger. They are not decorative brand colors.
6. **Avoid electric blue and orange.** Legacy values such as `#1E6CFF`, `#40A3FF`, `#78BAFF`, and `#F47A32` should not be introduced into redesigned desktop views. `remaining_pages_palette_v1.py` maps legacy literals into the new system where needed.
7. **Do not make every surface a card.** Prefer one composed workspace with spacing, hairlines, and hierarchy. Use raised surfaces only when they carry actual grouping/selection meaning.

## Persistent shell rules

Current navigation hierarchy:

**SESSION**
- Shot
- Club
- Table
- Numbers

**PRACTICE**
- Range

**TOOLS**
- Dispersion
- Bag
- Fit
- Lab
- Setup

Shell treatment:

- Section bands: deep teal (`#173B42`) with light text.
- Active nav: dark teal surface + gold left rail + light-gold icon + white label.
- Inactive nav: cool slate/teal-gray, never bright blue.
- Recent Shots selected card: raised navy/teal + gold left edge/current marker.
- New Session control: dark button with gold outline/gold `+`, not a large solid-color block.
- Preserve the dedicated collapsed-sidebar gutter so the reopen chevron never overlays the nav.

Reference implementation: `shell_redesign_v13.py` and `shell_redesign_v14.py`.

## Page-specific notes

- **Shot:** `overview_redesign_v15.py` is the accepted hierarchy/palette reference. Gold = current/emphasis; teal = analytical geometry. Session Trends intentionally alternate teal and gold. Fade in Shape Mix is gold.
- **Club:** `club_redesign_v3.py` owns the current visual treatment and measured/estimated credibility states. Keep one continuous page background; avoid cleanup rectangles that visually patch over a different base color.
- **Table:** `table_redesign_v2.py`. Current/selected row uses gold emphasis; structure stays teal/navy.
- **Numbers:** `numbers_redesign_v2.py`. Carry can remain the hero gold metric; supporting states/data should use teal/slate.
- **Dispersion:** `dispersion_redesign_v1.py` plus `remaining_pages_palette_v1.py`. Current shot = gold, analytical geometry = teal, guides = muted teal.
- **Range / Bag / Fit / Lab / Setup:** currently pass through `remaining_pages_palette_v1.py` so legacy production layouts inherit the accepted palette without a structural redesign.

## Data credibility rules

These are design requirements, not optional copy choices.

- Preserve **Measured / Derived / Estimated / Direction Estimate / Unavailable** distinctions.
- Never show fake precision for unavailable impact/location data.
- Derived or estimated club data must remain visibly identified as such.
- Do not style unavailable values like measured values.
- Preserve Nova/OpenGolfCoach calculation and confidence behavior unless explicitly changing product logic.

## Implementation guardrails

- Keep design work isolated from upstream production logic where practical.
- Preserve Nova connectivity, shot calculations, persistence, hardware, pressure capture, physics, and OpenGolfCoach enrichment unless a requirement explicitly changes them.
- Update hit-test geometry whenever clickable UI geometry moves. The design launcher intentionally hit-tests final design-owned rectangles before production rectangles.
- Keep the macOS cursor native (`arrow`), not `hand2`.
- Use the approved PNG branding assets; do not redraw the brand in code.
- Avoid a global `theme.py` color replacement on this branch unless the entire app/web surface is being migrated deliberately. Current desktop work is page-local to reduce regressions.
- Validate packaged builds before proposing the design work upstream.

## If you add or restyle a page

Start with these roles rather than choosing new colors:

```python
GOLD = "#D4A24F"       # current / selected / primary emphasis
GOLD_LIGHT = "#E3BC70" # active icon / small highlight
TEAL = "#32979A"       # supporting analysis
TEAL_LINE = "#58B7B4"  # chart / geometry stroke
TEAL_TEXT = "#78C4C1"  # analytical text
TEAL_SOFT = "#698E96"  # secondary analytical detail
PAGE_BG = "#0A2029"
SURFACE = "#0D2731"
SURFACE_2 = "#15333D"
HAIRLINE = "#2A4C55"
TEXT = "#F3F6FA"
TEXT_2 = "#B3BEC2"
TEXT_3 = "#70868C"
GUIDE = "#456D76"
```

Before inventing a new color, ask whether the element is **primary/current**, **analytical**, **structural**, **secondary**, **success**, or **danger**. It should almost always map to one of the roles above.
