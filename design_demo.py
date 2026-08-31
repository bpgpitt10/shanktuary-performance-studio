"""Design-only launcher with deterministic in-memory sample data.

This file exists only on the design branch. It never reads or writes the
normal session-history file, so screenshots and UI experiments cannot touch a
user's launch-monitor data. The production entry point remains
shanktuary_performance_studio.py.
"""

import math

import shanktuary_performance_studio as studio


def _shot(
    idx,
    club,
    carry,
    ball_speed,
    launch,
    spin,
    apex,
    descent,
    offline,
    spin_axis,
    club_path,
    face_to_path,
    shot_name,
):
    """Return one realistic-looking Nova/OGC-shaped shot for UI rendering."""
    smash = 1.39
    club_speed = ball_speed / smash
    total = carry + 5.5 + max(-1.0, min(2.0, ball_speed - 118.0)) * 0.15
    backspin = int(spin * math.cos(math.radians(spin_axis)))
    sidespin = int(spin * math.sin(math.radians(spin_axis)))
    horizontal_launch = max(-3.5, min(3.5, offline / 8.0))
    face_to_target = club_path + face_to_path

    return {
        "id": f"design-demo-{idx:02d}",
        "shot_id": f"design-demo-{idx:02d}",
        "timestamp": f"20:{38 + idx // 6:02d}:{(idx * 7) % 60:02d}",
        "club": club,
        "excluded": False,
        "ball_speed_meters_per_second": ball_speed / 2.2369362921,
        "vertical_launch_angle_degrees": launch,
        "horizontal_launch_angle_degrees": horizontal_launch,
        # Keep a root-level copy because the app's clamp detector reads here.
        "total_spin_rpm": spin,
        "open_golf_coach": {
            "us_customary_units": {
                "ball_speed_mph": ball_speed,
                "club_speed_mph": club_speed,
                "carry_distance_yards": carry,
                "total_distance_yards": total,
                "offline_distance_yards": offline,
                "peak_height_yards": apex,
                "optimal_maximum_distance_yards": carry + 8.0,
            },
            "smash_factor": smash,
            "total_spin_rpm": spin,
            "backspin_rpm": backspin,
            "sidespin_rpm": sidespin,
            "spin_axis_degrees": spin_axis,
            "club_path_degrees": club_path,
            "club_face_to_path_degrees": face_to_path,
            "club_face_to_target_degrees": face_to_target,
            "descent_angle_degrees": descent,
            "hang_time_seconds": 5.1 + (carry - 150.0) / 45.0,
            "distance_efficiency_percent": 94.0 + min(4.0, (carry % 5) * 0.7),
            "shot_name": shot_name,
            "shot_rank": "A" if abs(offline) <= 4.0 else "B",
            "face_closure_rate_dps": 2050.0 + idx * 17.0,
        },
    }


def build_demo_shots():
    """Build a multi-club session that exercises every shot-data view."""
    clubs = [
        # club, carry, ball, launch, spin, apex yds, descent
        ("7 Iron", 169.0, 119.5, 17.1, 6200, 34.0, 47.0),
        ("8 Iron", 154.0, 111.5, 18.8, 6900, 32.0, 49.0),
        ("6 Iron", 184.0, 126.0, 15.5, 5600, 36.0, 45.0),
    ]
    carry_delta = (-3.4, -1.4, 0.2, 1.7, 3.0)
    speed_delta = (-1.5, -0.7, 0.2, 0.8, 1.4)
    launch_delta = (0.7, -0.4, 0.1, -0.8, 0.4)
    spin_delta = (180, -120, 60, -210, 90)
    offlines = (-6.1, -2.5, 0.8, 4.2, -1.3)
    axes = (-5.4, -2.7, 1.0, 4.6, -1.5)
    paths = (2.8, 1.9, 1.2, -0.8, 2.1)
    face_paths = (-1.4, -0.8, 0.2, 1.5, -0.7)
    names = ("Draw", "Baby Draw", "Straight", "Soft Fade", "Baby Draw")

    shots = []
    idx = 1
    for club, base_carry, base_ball, base_launch, base_spin, base_apex, base_descent in clubs:
        for i in range(5):
            shots.append(
                _shot(
                    idx,
                    club,
                    base_carry + carry_delta[i],
                    base_ball + speed_delta[i],
                    base_launch + launch_delta[i],
                    base_spin + spin_delta[i],
                    base_apex + (i - 2) * 0.8,
                    base_descent + (i - 2) * 0.6,
                    offlines[i],
                    axes[i],
                    paths[i],
                    face_paths[i],
                    names[i],
                )
            )
            idx += 1

    # Finish on a clean 7-iron so Overview/Quad open on a representative shot.
    shots.append(
        _shot(
            idx,
            "7 Iron",
            171.6,
            120.7,
            16.8,
            6125,
            34.8,
            47.4,
            -1.8,
            -2.1,
            2.4,
            -0.9,
            "Baby Draw",
        )
    )
    return shots


def build_pressure_trace():
    """Deterministic synthetic pressure trace for the Swing Lab canvas."""
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

        # Four broad pressure cells: left toe, right toe, left heel, right heel.
        toe_bias = 0.53 + 0.08 * math.sin(t * math.pi)
        left_load = total_kg * lead / 100.0
        right_load = total_kg * trail / 100.0
        raw_cells = [
            left_load * toe_bias,
            right_load * toe_bias,
            left_load * (1.0 - toe_bias),
            right_load * (1.0 - toe_bias),
        ]
        frames.append(
            {
                "phase": phase,
                "total_kg": total_kg,
                "force_bw": force_bw,
                "pct_left": lead,
                "pct_right": trail,
                "torque_nm": torque,
                "cop_x": cop_x,
                "cop_y": cop_y,
                "raw_cells": raw_cells,
            }
        )
    return frames


class DesignDemoApp(studio.ShanktuaryApp):
    """Normal UI with a sandboxed, non-persistent design session."""

    def load_session_history(self):
        # Deliberately do not read the normal user history in a design build.
        if not self.bag:
            self.init_default_bag()

    def save_session_to_file(self):
        # Clicks can exclude shots, clear sessions, edit bag specs, etc. Keep
        # all of those experiments in memory so the demo can never alter disk.
        return

    def __init__(self, root):
        super().__init__(root)
        shots = build_demo_shots()
        self.sessions = [
            {
                "id": "design_demo_session",
                "name": "Design Demo · Multi-Club",
                "created_at": "Design baseline",
                "shots": shots,
            }
        ]
        self.active_session_index = 0
        self.current_club = "7 Iron"
        self.club_filter = "ALL"
        self.selected_shot_index = len(shots) - 1
        self.current_shot = shots[-1]
        self.view_mode = 9
        self.swing_lab_history = build_pressure_trace()

        # Give Swing Lab a populated current state as well as a historical
        # curve. If the pressure manager implementation changes, failure here
        # is harmless: the stored demo trace still renders the timelines.
        try:
            pm = getattr(studio.obs_server, "pressure_manager", None)
            if pm is not None:
                pm.latest_frame = self.swing_lab_history[-1]
        except Exception:
            pass

        root.title(
            f"Shanktuary Performance Studio {studio.APP_VERSION} · DESIGN DEMO"
        )
        self.draw_screen()


def main():
    # The browser/OBS range still needs its local server. We intentionally do
    # not start the Nova websocket worker in the design launcher: sample shots
    # are deterministic and this binary should never depend on hardware.
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

    app = DesignDemoApp(root)  # noqa: F841 - Tk callbacks retain this instance
    try:
        root.mainloop()
    except KeyboardInterrupt:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    main()
