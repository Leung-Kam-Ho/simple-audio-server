import os
import argparse
import threading

import pygame
from flask import Flask, jsonify, request

SUPPORTED_EXTENSIONS = {".mp3", ".ogg", ".wav", ".flac", ".m4a", ".aac"}

app = Flask(__name__)

sound_folder: str = ""
current_sound: pygame.mixer.Sound | None = None
is_playing: bool = False


def init_pygame():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)


def stop_current_sound():
    global current_sound, is_playing
    if current_sound and is_playing:
        current_sound.stop()
        current_sound = None
        is_playing = False


@app.route("/api/audio", methods=["GET"])
def list_audio():
    if not sound_folder or not os.path.isdir(sound_folder):
        return jsonify({"error": f"Sound folder not found: {sound_folder}"}), 404

    files = []
    for f in sorted(os.listdir(sound_folder)):
        ext = os.path.splitext(f)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            files.append(f)

    return jsonify({"folder": sound_folder, "files": files})


@app.route("/api/play/<path:filename>", methods=["GET", "POST"])
def play_sound(filename):
    global current_sound, is_playing

    if not sound_folder or not os.path.isdir(sound_folder):
        return jsonify({"error": f"Sound folder not found: {sound_folder}"}), 404

    file_path = os.path.join(sound_folder, filename)
    if not os.path.isfile(file_path):
        return jsonify({"error": f"File not found: {filename}"}), 404

    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return jsonify({"error": f"Unsupported format: {ext}"}), 400

    if is_playing:
        stop_current_sound()

    try:
        current_sound = pygame.mixer.Sound(file_path)
        current_sound.play()
        is_playing = True
        return jsonify({"status": "playing", "file": filename})
    except pygame.error as e:
        return jsonify({"error": f"Failed to play sound: {str(e)}"}), 500


@app.route("/api/stop", methods=["GET", "POST"])
def stop_sound():
    global is_playing
    stop_current_sound()
    return jsonify({"status": "stopped"})


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "folder": sound_folder,
        "is_playing": is_playing,
        "current_file": None,
    })


def parse_args():
    parser = argparse.ArgumentParser(description="Simple Audio Server")
    parser.add_argument(
        "--folder",
        "-f",
        required=True,
        help="Path to the folder containing audio files",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=5000,
        help="Port to bind (default: 5000)",
    )
    return parser.parse_args()


def main():
    global sound_folder
    args = parse_args()
    sound_folder = os.path.abspath(args.folder)

    if not os.path.isdir(sound_folder):
        print(f"Error: '{args.folder}' is not a valid directory.")
        return

    init_pygame()
    print(f"Audio server running on http://{args.host}:{args.port}")
    print(f"Sound folder: {sound_folder}")
    print(f"Endpoints:")
    print(f"  GET  /api/audio            - list all audio files")
    print(f"  GET  /api/play/<file>      - play a sound")
    print(f"  POST /api/play/<file>      - play a sound")
    print(f"  GET  /api/stop             - stop playback")
    print(f"  POST /api/stop             - stop playback")
    print(f"  GET  /api/status           - get current status")

    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
