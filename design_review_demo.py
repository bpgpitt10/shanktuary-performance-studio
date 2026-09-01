"""Final visual-review launcher for the current design sandbox.

Adds realistic club-specific demo dispersion, the polished Range view, and the
recomposed textured header without changing production data or connectivity.
"""

import design_overview_demo as current
import range_redesign_v2
import shell_redesign_v17


def build_review_shots():
    """Demo data whose clubs have intentionally different dispersion patterns."""
    specs = [
        {
            "club": "7 Iron", "carry": 169.0, "ball": 119.5, "launch": 17.1,
            "spin": 6200, "apex": 34.0, "descent": 47.0,
            "carry_d": (-4.6, -2.0, -0.7, 1.5, 3.4),
            "speed_d": (-1.4, -0.6, 0.2, 0.9, 1.3),
            "off": (-7.2, -3.4, 1.1, 5.3, -1.6),
            "axis": (-6.2, -3.3, 1.1, 5.1, -1.8),
            "path": (3.1, 2.4, 1.3, -0.4, 2.2),
            "face": (-1.6, -1.0, 0.2, 1.7, -0.8),
            "names": ("Draw", "Baby Draw", "Straight", "Soft Fade", "Baby Draw"),
        },
        {
            "club": "8 Iron", "carry": 154.0, "ball": 111.5, "launch": 18.8,
            "spin": 6900, "apex": 32.0, "descent": 49.0,
            "carry_d": (-2.3, -1.1, -0.1, 0.9, 1.8),
            "speed_d": (-0.9, -0.4, 0.1, 0.5, 0.8),
            "off": (-2.8, -1.0, 0.4, 1.8, -0.6),
            "axis": (-3.0, -1.2, 0.5, 2.0, -0.8),
            "path": (1.8, 1.4, 0.9, 0.3, 1.1),
            "face": (-0.9, -0.5, 0.1, 0.7, -0.4),
            "names": ("Baby Draw", "Baby Draw", "Straight", "Soft Fade", "Straight"),
        },
        {
            "club": "6 Iron", "carry": 184.0, "ball": 126.0, "launch": 15.5,
            "spin": 5600, "apex": 36.0, "descent": 45.0,
            "carry_d": (-6.0, -3.2, 0.6, 2.8, 5.2),
            "speed_d": (-2.1, -1.0, 0.2, 1.2, 1.9),
            "off": (10.2, 6.8, 3.1, -1.9, 5.6),
            "axis": (7.4, 5.2, 2.7, -1.4, 4.8),
            "path": (-2.3, -1.7, -0.8, 0.5, -1.2),
            "face": (2.0, 1.5, 0.9, -0.3, 1.3),
            "names": ("Fade", "Soft Fade", "Baby Fade", "Straight", "Soft Fade"),
        },
    ]

    shots = []
    idx = 1
    for spec in specs:
        for i in range(5):
            shots.append(
                current.base._shot(
                    idx,
                    spec["club"],
                    spec["carry"] + spec["carry_d"][i],
                    spec["ball"] + spec["speed_d"][i],
                    spec["launch"] + (0.6, -0.4, 0.1, -0.7, 0.4)[i],
                    spec["spin"] + (170, -130, 55, -205, 95)[i],
                    spec["apex"] + (i - 2) * 0.8,
                    spec["descent"] + (i - 2) * 0.6,
                    spec["off"][i],
                    spec["axis"][i],
                    spec["path"][i],
                    spec["face"][i],
                    spec["names"][i],
                )
            )
            idx += 1

    # Finish on the familiar representative shot used throughout the design pass.
    shots.append(
        current.base._shot(
            idx, "7 Iron", 171.6, 120.7, 16.8, 6125, 34.8, 47.4,
            -1.8, -2.1, 2.4, -0.9, "Baby Draw",
        )
    )
    return shots


class ReviewDesignApp(current.OverviewDesignApp):
    def __init__(self, root):
        super().__init__(root)
        shots = build_review_shots()
        self.sessions[0]["shots"] = shots
        self.selected_shot_index = len(shots) - 1
        self.current_shot = shots[-1]
        self.current_club = "7 Iron"
        self.club_filter = "ALL"
        self.draw_screen()

    def draw_3d_range_viewport(self, *args, **kwargs):
        return range_redesign_v2.draw_range(self, *args, **kwargs)

    def draw_top_header(self, w, h, offset_x=0):
        # Paint production once for state/compatibility, then make v17 the only
        # visible header treatment. v17 fully covers the 52px ribbon.
        current.base.studio.ShanktuaryApp.draw_top_header(
            self, w, h, offset_x=offset_x
        )
        shell_redesign_v17.paint_top_header(self, w, h, offset_x=offset_x)


def main():
    current.base.studio.obs_server.launch_obs_server_thread()

    root = current.base.studio.tk.Tk()
    default_w, default_h = 1920, 1080
    scr_w = root.winfo_screenwidth()
    scr_h = root.winfo_screenheight()
    if scr_w >= default_w and scr_h >= default_h:
        win_w, win_h = default_w, default_h
    else:
        win_w = min(default_w, scr_w - 40)
        win_h = min(default_h, scr_h - 80)
    pos_x = max(0, (scr_w - win_w) // 2)
    pos_y = max(0, (scr_h - win_h) // 3)
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    root.minsize(1100, 720)

    app = ReviewDesignApp(root)  # noqa: F841
    try:
        root.mainloop()
    except KeyboardInterrupt:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    main()
