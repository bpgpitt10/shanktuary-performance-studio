#!/usr/bin/env python3
"""Non-persistent UI review launcher for the integrated production desktop.

This uses the exact same ShanktuaryDesktopApp as production, but seeds a small
in-memory multi-club session so visual review does not require Nova hardware.
It never reads or writes the user's normal session history.
"""

from __future__ import annotations

import math

import shanktuary_performance_studio as studio
from src.ui import ShanktuaryDesktopApp


def _shot(idx, club, carry, ball, launch, spin, apex, offline, axis, path, ftp, name):
    smash = 1.39
    club_speed = ball / smash
    total = carry + 5.7
    return {
        "id": f"integration-review-{idx}",
        "shot_id": f"integration-review-{idx}",
        "timestamp": f"20:4{idx // 10}:{(idx * 7) % 60:02d}",
        "club": club,
        "excluded": False,
        "ball_speed_meters_per_second": ball / 2.2369362921,
        "vertical_launch_angle_degrees": launch,
        "horizontal_launch_angle_degrees": max(-3.5, min(3.5, offline / 8.0)),
        "total_spin_rpm": spin,
        "open_golf_coach": {
            "us_customary_units": {
                "ball_speed_mph": ball,
                "club_speed_mph": club_speed,
                "carry_distance_yards": carry,
                "total_distance_yards": total,
                "offline_distance_yards": offline,
                "peak_height_yards": apex,
            },
            "smash_factor": smash,
            "total_spin_rpm": spin,
            "backspin_rpm": int(spin * math.cos(math.radians(axis))),
            "sidespin_rpm": int(spin * math.sin(math.radians(axis))),
            "spin_axis_degrees": axis,
            "club_path_degrees": path,
            "club_face_to_path_degrees": ftp,
            "club_face_to_target_degrees": path + ftp,
            "descent_angle_degrees": 47.0,
            "hang_time_seconds": 5.4,
            "shot_name": name,
            "shot_rank": "A" if abs(offline) < 4 else "B",
            "face_closure_rate_dps": 2050.0 + idx * 13,
        },
    }


def build_review_shots():
    specs = [
        ("6 Iron", 184.0, 126.0, 15.5, 5600, 36.0,
         [(-3.0, -5.8), (0.8, -2.2), (2.4, 1.1), (4.7, 4.8), (1.5, 2.5)]),
        ("7 Iron", 169.0, 119.5, 17.1, 6200, 34.0,
         [(-2.8, -4.2), (-0.9, -1.4), (0.4, 0.7), (2.1, 2.9), (3.2, -0.8)]),
        ("8 Iron", 154.0, 111.5, 18.8, 6900, 32.0,
         [(-1.7, -2.2), (-0.5, -0.5), (0.3, 0.9), (1.0, 1.5), (1.8, -0.3)]),
    ]
    shots = []
    idx = 1
    for club, base_carry, base_ball, base_launch, base_spin, base_apex, pattern in specs:
        for i, (carry_delta, offline) in enumerate(pattern):
            axis = offline * 0.8
            path = 2.4 - i * 0.45
            ftp = -0.9 + i * 0.35
            name = "Baby Draw" if offline <= 0 else ("Straight" if offline < 1.2 else "Soft Fade")
            shots.append(_shot(
                idx, club, base_carry + carry_delta, base_ball + (i - 2) * 0.55,
                base_launch + (2 - i) * 0.18, base_spin + (i - 2) * 70,
                base_apex + (i - 2) * 0.6, offline, axis, path, ftp, name,
            ))
            idx += 1

    shots.append(_shot(
        idx, "7 Iron", 171.6, 120.7, 16.8, 6125, 34.8, -1.8,
        -2.1, 2.4, -0.9, "Baby Draw",
    ))
    return shots


class ReviewApp(ShanktuaryDesktopApp):
    def load_session_history(self):
        # Deliberately bypass on-disk user data.
        if not getattr(self, "bag", None):
            self.init_default_bag()

    def save_session_to_file(self):
        # All review interactions remain in memory.
        return

    def __init__(self, root):
        super().__init__(root)
        shots = build_review_shots()
        self.sessions = [{
            "id": "integration_review",
            "name": "Integration Review · Multi-Club",
            "created_at": "Review fixture",
            "shots": shots,
        }]
        self.active_session_index = 0
        self.current_club = "7 Iron"
        self.club_filter = "ALL"
        self.selected_shot_index = len(shots) - 1
        self.current_shot = shots[-1]
        self.view_mode = 9
        root.title(f"Shanktuary Performance Studio {studio.APP_VERSION} · UI REVIEW")
        self.draw_screen()


def main():
    # Browser/range surfaces still work, but do not attempt Nova discovery.
    studio.obs_server.launch_obs_server_thread()

    root = studio.tk.Tk()
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

    app = ReviewApp(root)  # noqa: F841
    try:
        root.mainloop()
    except KeyboardInterrupt:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    main()
