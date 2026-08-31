"""Overview-redesign launcher for the isolated design sandbox."""

import math

import design_demo as base
import overview_redesign


class OverviewDesignApp(base.DesignDemoApp):
    """Design demo with the new Overview renderer only."""

    def draw_overview_viewport(self, *args, **kwargs):
        return overview_redesign.draw_overview(self, *args, **kwargs)

    def __init__(self, root):
        super().__init__(root)

        # Make the deterministic demo's start-line data agree with its named
        # draw/fade shapes. This only changes in-memory sandbox shots and gives
        # the new Start -> Movement -> Landing visual something meaningful to
        # demonstrate.
        for shot in self.session_shots:
            ogc = shot.get("open_golf_coach", {}) or {}
            axis = float(ogc.get("spin_axis_degrees") or 0.0)
            offline = float((ogc.get("us_customary_units", {}) or {}).get(
                "offline_distance_yards") or 0.0)
            # Negative spin axis (left-curving for RH) begins modestly right;
            # positive axis begins modestly left. A tiny finish-line term keeps
            # nearly straight shots from looking artificially reversed.
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
