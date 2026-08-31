"""Tenth-pass Shot wrapper: keep v9 shot-analysis polish, restore the accepted v8 session area."""

import overview_redesign_v8 as v8
import overview_redesign_v9 as v9


def draw_overview(*args, **kwargs):
    """Use the v9 live-shot changes, but roll the session review back to v8."""
    v9._session_surface = v8._session_surface
    v9._draw_session_bottom = v8._draw_session_bottom
    return v9.draw_overview(*args, **kwargs)
