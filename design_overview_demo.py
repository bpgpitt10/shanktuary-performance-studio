"""Shot-view redesign launcher for the isolated sanctuary-brand sandbox."""

import design_demo as base
import overview_redesign_v8
import shell_redesign_v10
import theme


class OverviewDesignApp(base.DesignDemoApp):
    """Design demo with the experimental Shot view and sanctuary brand treatment."""

    @staticmethod
    def _hit(rect, x, y):
        return bool(rect and rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3])

    def _toggle_design_sidebar(self):
        """Own the Recent Shots drawer state entirely in the design sandbox.

        Production's toggle path also owns legacy hamburger/header geometry.
        Mixing that state machine with the repainted design shell caused the
        drawer to close but intermittently fail to reopen. The design demo now
        flips only the actual collapsed state and redraws from one source of
        truth.
        """
        self.sidebar_collapsed = not bool(getattr(self, "sidebar_collapsed", False))
        self.show_session_menu = False
        self.show_filter_menu = False
        self.show_club_menu = False
        self.show_tools_menu = False
        self.sidebar_width = 300
        self.draw_screen()

    def draw_overview_viewport(self, *args, **kwargs):
        return overview_redesign_v8.draw_overview(self, *args, **kwargs)

    def draw_left_sidebar(self, w, h):
        super().draw_left_sidebar(w, h)
        shell_redesign_v10.paint_sidebar(self, w, h)

    def draw_nav_rail(self, h):
        super().draw_nav_rail(h)
        shell_redesign_v10.paint_nav(self, h)

    def draw_top_header(self, w, h, offset_x=0):
        super().draw_top_header(w, h, offset_x=offset_x)
        shell_redesign_v10.paint_top_header(self, w, h, offset_x=offset_x)

    def handle_mouse_press(self, event):
        """Hit-test the FINAL design shell before production's mutable rectangles."""
        x, y = event.x, event.y

        # Drawer toggle gets a redundant geometry-independent hit zone as well
        # as the painted design rect. This makes the full visible chevron/tab
        # responsive even if a legacy production draw mutates shared geometry.
        if getattr(self, "sidebar_collapsed", False):
            drawer_hotzone = (0, 52, theme.RAIL_W + 28, 96)
        else:
            drawer_hotzone = (self.sidebar_width - 48, 138,
                              self.sidebar_width + 8, 194)

        if (self._hit(getattr(self, "design_sidebar_toggle_rect", None), x, y)
                or self._hit(drawer_hotzone, x, y)):
            self._toggle_design_sidebar()
            return

        if not getattr(self, "sidebar_collapsed", False):
            for x1, y1, x2, y2, shot_idx in getattr(self, "design_shot_card_rects", []):
                if x1 <= x <= x2 and y1 <= y <= y2:
                    if 0 <= shot_idx < len(self.session_shots):
                        self.selected_shot_index = shot_idx
                        self.current_shot = self.session_shots[shot_idx]
                        self.show_club_menu = False
                        self.show_tools_menu = False
                        self.draw_screen()
                    return

        for mode_id, rect in getattr(self, "design_mode_rects", {}).items():
            if self._hit(rect, x, y):
                self.show_club_menu = False
                self.show_tools_menu = False
                self.set_mode(mode_id)
                return

        if self._hit(getattr(self, "design_club_btn_rect", None), x, y):
            self.show_club_menu = not getattr(self, "show_club_menu", False)
            self.show_tools_menu = False
            self.draw_screen()
            return

        if self._hit(getattr(self, "design_dexterity_btn_rect", None), x, y):
            self.is_left_handed = not getattr(self, "is_left_handed", False)
            self.show_club_menu = False
            self.show_tools_menu = False
            self.draw_screen()
            return

        if self._hit(getattr(self, "design_tools_btn_rect", None), x, y):
            self.show_tools_menu = not getattr(self, "show_tools_menu", False)
            self.show_club_menu = False
            self.draw_screen()
            return

        if self._hit(getattr(self, "design_fullscreen_btn_rect", None), x, y):
            self.toggle_fullscreen()
            return

        return super().handle_mouse_press(event)

    def __init__(self, root):
        self.design_sidebar_toggle_rect = None
        self.design_shot_card_rects = []
        self.design_mode_rects = {}
        self.design_club_btn_rect = None
        self.design_dexterity_btn_rect = None
        self.design_tools_btn_rect = None
        self.design_fullscreen_btn_rect = None

        super().__init__(root)

        self.sidebar_width = 300
        self.canvas.config(cursor="arrow")
        self.canvas.bind(
            "<Motion>",
            lambda _event: self.canvas.config(cursor="arrow"),
            add="+",
        )

        for shot in self.session_shots:
            ogc = shot.get("open_golf_coach", {}) or {}
            axis = float(ogc.get("spin_axis_degrees") or 0.0)
            offline = float((ogc.get("us_customary_units", {}) or {}).get(
                "offline_distance_yards") or 0.0)
            h_launch = -axis * 0.18 + offline * 0.01
            shot["horizontal_launch_angle_degrees"] = max(-3.5, min(3.5, h_launch))

        if self.session_shots:
            self.current_shot = self.session_shots[self.selected_shot_index]
        root.title(f"Shanktuary {base.studio.APP_VERSION} · SANCTUARY BRAND PASS")
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
