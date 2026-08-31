"""Overview-redesign launcher for the isolated design sandbox."""

import math

import design_demo as base
import overview_redesign_v5
import shell_redesign_v4


class OverviewDesignApp(base.DesignDemoApp):
    """Design demo with the experimental Overview and shell treatment."""

    def draw_overview_viewport(self, *args, **kwargs):
        return overview_redesign_v5.draw_overview(self, *args, **kwargs)

    def draw_left_sidebar(self, w, h):
        # Let production register all normal click targets, then repaint the
        # design shell over it without changing session behavior.
        super().draw_left_sidebar(w, h)
        shell_redesign_v4.paint_sidebar(self, w, h)

    def draw_nav_rail(self, h):
        super().draw_nav_rail(h)
        shell_redesign_v4.paint_nav(self, h)

    def __init__(self, root):
        super().__init__(root)

        # Give Recent Shots enough width for the compact/expanded hierarchy in
        # the accepted mockup. Production remains untouched on this branch.
        self.sidebar_width = 330

        # Tk's hand2 cursor renders as a goofy left-pointing glove on macOS.
        # Keep the native arrow everywhere; selection/hover styling carries the
        # interaction affordance instead.
        self.canvas.config(cursor="arrow")
        self.canvas.bind(
            "<Motion>",
            lambda _event: self.canvas.config(cursor="arrow"),
            add="+",
        )

        # Make the deterministic demo's start-line data agree with its named
        # draw/fade shapes. This only changes in-memory sandbox shots and gives
        # the Start -> Movement -> Landing visual something meaningful to show.
        for shot in self.session_shots:
            ogc = shot.get("open_golf_coach", {}) or {}
            axis = float(ogc.get("spin_axis_degrees") or 0.0)
            offline = float((ogc.get("us_customary_units", {}) or {}).get(
                "offline_distance_yards") or 0.0)
            h_launch = -axis * 0.18 + offline * 0.01
            shot["horizontal_launch_angle_degrees"] = max(-3.5, min(3.5, h_launch))

        if self.session_shots:
            self.current_shot = self.session_shots[self.selected_shot_index]
        root.title(f"Shanktuary {base.studio.APP_VERSION} · OVERVIEW DESIGN DEMO")
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
