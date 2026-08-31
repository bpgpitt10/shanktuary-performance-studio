# Design Pass Baseline

This branch is reserved for visual/design work only until explicitly expanded.

Baseline established from the fork's current main line before any visual changes.

- App version in source: v1.3.1
- Branch: feature/design-pass
- Primary desktop UI: shanktuary_performance_studio.py + theme.py
- Browser theme source of truth: theme.py -> scripts/gen_theme_css.py -> assets/theme.css

Design-pass guardrails:
- Preserve Nova connectivity, shot calculations, persistence, hardware, pressure capture, and physics unless a design requirement explicitly demands a change.
- Preserve measured / derived / estimated data semantics.
- Update hit-test geometry whenever clickable UI geometry moves.
- Validate desktop builds before proposing changes upstream.
