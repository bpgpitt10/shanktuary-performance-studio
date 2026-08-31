"""Shot-view redesign launcher for the isolated design sandbox."""

import math

import design_demo as base
import overview_redesign_v7
import shell_redesign_v7


class OverviewDesignApp(base.DesignDemoApp):
    """Design demo with the experimental Shot view and shell treatment."""

    def draw_overview_viewport(self, *args, **kwargs):
        return overview_redesign_v7.draw_overview(self, *args, **kwargs)

    def draw_left_sidebar(self, w, h):
        # Production registers the normal interaction hooks; the design shell
        # repaints them and, in v7, deliberately replaces the hit rectangles
        # where the visual controls differ from production.
        super().draw_left_sidebar(w, h)
        shell_redesign_v7.paint_sidebar(self, w, h)

    def draw_nav_rail(self, h):
        super().draw_nav_rail(h)
        shell_redesign_v7.paint_nav(self, h)

    def draw_top_header(self, w, h, offset_x=0):
        super().draw_top_header(w, h, offset_x=offset_x)
        shell_redesign_v7.paint_top_header(self, w, h, offset_x=offset_x)

    def __init__(self, root):
        super().__init__(root)

        # Slightly narrower Recent Shots rail; the persistent collapse/reopen
        # control makes reclaiming the entire rail an intentional interaction.
        self.sidebar_width = 300

        # Tk's hand2 cursor renders as a goofy left-pointing glove on macOS.
        self.canvas.config(cursor="arrow")
        self.canvas.bind(
            "<Motion>",
            lambda _event: self.canvas.config(cursor="arrow"),
            add="+",
        )

        # Make deterministic demo start-line data agree with named draw/fade
        # shapes. This only changes in-memory sandbox shots.
        for shot in self.session_shots:
            ogc = shot.get("open_golf_coach", {}) or {}
            axis = float(ogc.get("spin_axis_degrees") or 0.0)
            offline = float((ogc.get("us_customary_units", {}) or {}).get(
                "offline_distance_yards") or 0.0)
            h_launch = -axis * 0.18 + offline * 0.01
            shot["horizontal_launch_angle_degrees"] = max(-3.5, min(3.5, h_launch))

        if self.session_shots:
            self.current_shot = self.session_shots[self.selected_shot_index]
        root.title(f"Shanktuary {base.studio.APP_VERSION} · SHOT DESIGN DEMO")
        self.draw_screen()


def main():
    base.studio.obs_server.launch_obs_server_thread()

    root = base.studio.tk.Tk()
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

    app = OverviewDesignApp(root)  # noqa: F841
    try:
        root.mainloop()
    except KeyboardInterrupt:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    main()
