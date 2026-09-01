# Shanktuary Performance Studio

> **Launch monitor visualization, performance analysis, and streaming tools for OpenLaunch Nova & OpenGolfCoach.**

## Desktop app

The redesigned production desktop entry point is:

```bash
python3 shanktuary_app.py
```

`shanktuary_app.py` starts the normal Nova websocket worker and OBS/browser server, then instantiates `src.ui.ShanktuaryDesktopApp`. The hardware, OpenGolfCoach processing, aim calibration, persistence, pressure capture, and browser/API implementation remain in `shanktuary_performance_studio.py`; the UI subclass changes desktop rendering and hit geometry only.

For visual conventions and maintainership guidance, see [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md).

## Quick start

```bash
git clone https://github.com/ShanktuaryGolf/shanktuary-performance-studio.git
cd shanktuary-performance-studio
pip install -r requirements.txt
python3 shanktuary_app.py
```

## Core capabilities

- Zero-config Nova discovery over `_openlaunch-ws._tcp.local.`
- OpenGolfCoach enrichment and launch-monitor analytics
- Aim calibration for a launch monitor that is not square to target
- Shot, Club, Table, Numbers, Range, Dispersion, Bag, Fit, Lab, and Setup desktop workspaces
- Wii Balance Board pressure capture and Swing Lab tooling
- Local OBS/browser overlay server on port `9321`
- WebGPU 3D range at `http://localhost:9321/range`
- Floor divot/projector surfaces and configurable browser overlays

## OBS & browser source URLs

- Clean OBS Browser Source: `http://localhost:9321`
- Floor Projector — Divot only: `http://localhost:9321/divot`
- Floor Projector — Metric tiles only: `http://localhost:9321/tiles`
- Floor Projector — Whole layout: `http://localhost:9321/?mode=projector`
- Web Configurator: `http://localhost:9321/config`
- Drag & Drop Canvas Editor: `http://localhost:9321/?edit=true`
- WebGPU 3D Driving Range: `http://localhost:9321/range`

## Desktop navigation

**SESSION** — Shot, Club, Table, Numbers  
**PRACTICE** — Range  
**TOOLS** — Dispersion, Bag, Fit, Lab, Setup

## Development

Run the full test suite before merging:

```bash
pytest -q
```

The cross-platform GitHub Actions workflow runs tests before building Linux, Windows, and macOS packages.

### UI implementation note

The public desktop seam is `src/ui/desktop.py`. The approved renderer snapshot currently lives under `src/ui/_legacy/` so the iterative `v1...v17` history does not pollute the repository root or the production data layer. New code should not import those files directly; use `ShanktuaryDesktopApp` and the roles in `src/ui/tokens.py`. As views are revisited, renderer internals can be consolidated without changing production call sites.

## License & credits

Developed by **Shanktuary Golf** for OpenLaunch Nova & OpenGolfCoach systems. Distributed under the MIT License.

### 3D asset attribution

The WebGPU 3D Driving Range ships the following models under **CC-BY-4.0**:

- **Pine tree** — Andriy Shekh
- **Wooden Sign With Roof** — KenVeel

Rendering uses three.js (MIT).
