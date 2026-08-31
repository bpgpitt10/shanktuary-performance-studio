"""Runtime palette role overrides for the isolated design sandbox.

The shared theme makes antique gold the primary brand accent. This module
reassigns analytical geometry that previously borrowed the primary blue so
charts and motion cues use the new muted teal secondary accent instead.
"""

import theme
import dispersion_redesign_v1 as dispersion
import overview_redesign_v4 as ov4
import overview_redesign_v7 as ov7
import overview_redesign_v12 as ov12


def apply():
    # Shot workspace: current-shot emphasis is gold; geometry/data is teal.
    ov4.BLUE = theme.ACCENT
    ov4.BLUE_LINE = theme.DATA_LINE
    ov4.BLUE_TEXT = theme.DATA_TEXT
    ov4.ORANGE = theme.ACCENT

    ov7.BLUE = theme.ACCENT
    ov7.BLUE_LINE = theme.DATA_LINE
    ov7.BLUE_TEXT = theme.DATA_TEXT
    ov7.ORANGE = theme.ACCENT
    ov7.GOLD = theme.ACCENT
    ov7.SESSION_DOT = ov7._mix(theme.TEXT_3, theme.DATA, .16)
    ov7.ELLIPSE = ov7._mix(theme.DATA_LINE, theme.BG, .34)
    ov7.NEUTRAL_POINT = ov7._mix(theme.TEXT_2, theme.DATA, .08)

    ov12.BLUE_LINE = theme.DATA_LINE
    ov12.BLUE_TEXT = theme.DATA_TEXT
    ov12.ORANGE = theme.ACCENT

    # Dedicated Dispersion tool: teal analysis, gold current shot.
    dispersion.BLUE = theme.DATA_LINE
    dispersion.BLUE_TEXT = theme.DATA_TEXT
    dispersion.ORANGE = theme.ACCENT


apply()
