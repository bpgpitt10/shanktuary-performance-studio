#!/usr/bin/env python3
"""Render-smoke the integrated review fixture's Tools pages.

Runs under xvfb in CI. This is intentionally a visual-fixture smoke test rather
than a production behavior test: each tool must render both its page chrome and
seeded review data so a downloaded UI-review build is actually inspectable.
"""

from __future__ import annotations

import tkinter as tk

from review_app import ReviewApp


def _canvas_texts(app):
    out = []
    for item in app.canvas.find_all():
        if app.canvas.type(item) != "text":
            continue
        text = app.canvas.itemcget(item, "text")
        if text:
            out.append(text)
    return out


def main():
    root = tk.Tk()
    root.geometry("1600x1000+0+0")
    root.update_idletasks()
    app = ReviewApp(root)
    root.update_idletasks()

    checks = {
        3: ("Dispersion", ("7 Iron", "Club Gapping")),
        6: ("Bag", ("7 Iron",)),
        7: ("Fit", ("7 Iron",)),
        8: ("Lab", ("Pressure",)),
        10: ("Setup", ("Setup",)),
    }

    failures = []
    for mode, (label, needles) in checks.items():
        app.set_mode(mode)
        root.update_idletasks()
        texts = _canvas_texts(app)
        joined = " | ".join(texts)
        print(f"[{label}] canvas_items={len(app.canvas.find_all())} text_items={len(texts)}")
        print(f"[{label}] sample={joined[:1200]}")
        missing = [needle for needle in needles if needle.lower() not in joined.lower()]
        if missing:
            failures.append(f"{label}: missing {missing}")

    root.destroy()
    if failures:
        raise SystemExit("Tool review smoke failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
