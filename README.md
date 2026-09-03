simple-audio-server

A simple Flask audio server with pygame playback.

## Installation

```bash
pip install .
# or with uv
uv pip install .
```

## Usage

```bash
simple_audio_server --folder ./sounds
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--folder`, `-f` | Path to the folder containing audio files | (required) |
| `--host` | Host to bind | `0.0.0.0` |
| `--port`, `-p` | Port to bind | `5000` |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/audio` | List all audio files |
| GET/POST | `/api/play/<filename>` | Play a sound |
| GET/POST | `/api/stop` | Stop playback |
| GET | `/api/status` | Get current status |

### Examples

```bash
# List audio files
curl http://localhost:5000/api/audio

# Play a sound
curl http://localhost:5000/api/play/alert.mp3

# Stop playback
curl http://localhost:5000/api/stop
```

## Supported Formats

`.mp3`, `.ogg`, `.wav`, `.flac`, `.m4a`, `.aac`
