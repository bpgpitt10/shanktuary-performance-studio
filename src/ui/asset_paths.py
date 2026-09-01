"""Resolve desktop UI assets in both source checkouts and PyInstaller bundles."""

from __future__ import annotations

import sys
from pathlib import Path


def asset_dir() -> Path:
    """Return the shared ``assets`` directory for this running app.

    PyInstaller one-dir apps expose bundled data under ``sys._MEIPASS``. Source
    runs keep assets at the repository root. Keep the packaged lookup first so
    renderers never accidentally walk out of the app bundle on macOS/Windows.
    """
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        bundled = Path(meipass) / "assets"
        if bundled.exists():
            return bundled

    here = Path(__file__).resolve()
    # src/ui/asset_paths.py -> repository root
    source = here.parents[2] / "assets"
    if source.exists():
        return source

    # Defensive fallback for unusual editable/install layouts.
    for parent in here.parents:
        candidate = parent / "assets"
        if candidate.exists():
            return candidate

    return source


def asset_path(name: str) -> str:
    return str(asset_dir() / name)
