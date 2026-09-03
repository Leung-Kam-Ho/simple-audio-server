# simple-audio-server

## Quick Start

```bash
uv run simple_audio_server --folder ./sounds
# or: uv run main.py --folder ./sounds
```

## Architecture

- `simple_audio_server/app.py` — Flask server, CLI entry point, client functions
- `simple_audio_server/templates/` — Web UI
- `simple_audio_server/__init__.py` — re-exports `main`, `play`, `stop`, `status`
- `main.py` — convenience wrapper to run the server

## Key Facts

- **Default port:** `4410` (not 5000)
- **CLI:** `simple_audio_server --folder PATH [--host HOST] [--port PORT]`
- **Python client:** `from simple_audio_server import play, stop, status` — these call the server API via `requests`, not local pygame
- **Pygame** runs only on the server side for audio playback
- **Web UI** at `/` lists audio files and provides play/stop buttons

## Versioning

Update `pyproject.toml [project] version` after every release. The version is printed at startup via `importlib.metadata.version()`.

## Build / Install

```bash
uv pip install .        # install from local
uv pip install . --upgrade  # update deps
```

Builds with hatchling. No tests or linters configured.

## Common Mistakes

- Don't confuse `play()`/`stop()`/`status()` (client functions that HTTP-call the server) with the internal `_play_sound_on_server()` (local pygame playback on the server)
- Don't use port `5000` — default is `4410`
- `simple_audio_server` CLI requires `--folder`; it is not optional
- When adding/removing dependencies, run `uv lock --upgrade-package <name>` then `uv sync`
