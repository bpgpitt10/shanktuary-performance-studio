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
                "apex_height_yards": apex,
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


def build_pressure_trace():
    """Create a deterministic, realistic pressure trace for Lab/Setup review."""
    frames = []
    for i in range(120):
        t = i / 119.0
        if t < 0.14:
            phase = "Address"
            lead = 50.0
        elif t < 0.43:
            phase = "Backswing"
            u = (t - 0.14) / 0.29
            lead = 50.0 - 14.0 * u
        elif t < 0.52:
            phase = "Transition"
            u = (t - 0.43) / 0.09
            lead = 36.0 + 13.0 * u
        elif t < 0.69:
            phase = "Downswing"
            u = (t - 0.52) / 0.17
            lead = 49.0 + 30.0 * u
        elif t < 0.73:
            phase = "Impact"
            lead = 80.0
        else:
            phase = "Follow Through"
            u = (t - 0.73) / 0.27
            lead = 80.0 - 9.0 * u

        impact_bump = math.exp(-((t - 0.71) / 0.055) ** 2)
        force_bw = 0.98 + 0.78 * impact_bump
        total_kg = 78.5 * force_bw
        trail = 100.0 - lead
        cop_x = (lead - 50.0) * -1.65
        cop_y = 18.0 * math.sin((t - 0.18) * math.pi * 1.6)
        torque = 10.0 * math.sin((t - 0.34) * math.pi * 2.2)
        toe_bias = 0.53 + 0.08 * math.sin(t * math.pi)
        left_load = total_kg * lead / 100.0
        right_load = total_kg * trail / 100.0

        frames.append({
            "timestamp": t * 2.4,
            "phase": phase,
            "total_kg": total_kg,
            "force_bw": force_bw,
            "pct_left": lead,
            "pct_right": trail,
            "left_pct": lead,
            "right_pct": trail,
            "left_kg": left_load,
            "right_kg": right_load,
            "torque_nm": torque,
            "cop_x": cop_x,
            "cop_y": cop_y,
            "raw_cells": [
                left_load * toe_bias,
                right_load * toe_bias,
                left_load * (1.0 - toe_bias),
                right_load * (1.0 - toe_bias),
            ],
        })
    return frames


class ReviewApp(ShanktuaryDesktopApp):
    def load_session_history(self):
        # Deliberately bypass on-disk user data.
        if not getattr(self, "bag", None):
            self.init_default_bag()

    def save_session_to_file(self):
        # All review interactions remain in memory.
        return

    def _seed_tool_review_state(self, shots):
        """Populate every analysis tool without touching production storage."""
        # Dispersion already reads the active session; pin a deterministic scope.
        self.dispersion_selected_club = "ALL"
        self.dispersion_view_submode = "split"

        # Bag reads the normal bag + active-session shot stats. Guarantee the
        # default bag exists even if production initialization changes later.
        if not getattr(self, "bag", None):
            self.init_default_bag()
        self.bag_scope = "session"
        self.bag_scroll_offset = 0

        # Fit intentionally starts with no clubs selected in production. The
        # review fixture selects the three clubs that have sample shots.
        self.fitting_selected_clubs = ["6 Iron", "7 Iron", "8 Iron"]
        self.fitting_baseline_club = "7 Iron"
        self.fitting_submode = "split"

        # Lab needs captured pressure data, which a hardware-free review build
        # would never receive naturally. Keep the trace inline on the selected
        # shot so get_pressure_trace() uses it without touching the trace store.
        trace = build_pressure_trace()
        self.swing_lab_history = trace
        self.current_shot["pressure_trace"] = trace
        try:
            metrics = studio.derive_pressure_metrics(trace)
            if metrics:
                self.current_shot["pressure_metrics"] = metrics
        except Exception:
            pass

        # Setup should be visually inspectable too. Use the built-in simulator
        # only in this review launcher; production remains hardware-driven.
        pm = getattr(studio.obs_server, "pressure_manager", None)
        if pm is not None:
            try:
                pm.set_simulator(True)
            except Exception:
                pass
            try:
                pm.set_board_mode("dual")
            except Exception:
                pass
            pm.assigned_left = "Review Board L"
            pm.assigned_right = "Review Board R"
            pm.latest_frame = trace[-1]
            pm.last_shot_trace = trace

        self.nova_connected = True

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
        self._seed_tool_review_state(shots)
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
