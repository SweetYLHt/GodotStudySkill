"""Local file handler — extract audio from a local video file."""

import os
import subprocess
from typing import Optional

from models import AudioMeta

def download_audio(file_path: str, output_dir: str) -> AudioMeta:
    """Convert a local video file to mp3 and return metadata."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Local file not found: {file_path}")

    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    mp3_path = os.path.join(output_dir, f"{base_name}.mp3")

    if not os.path.exists(mp3_path):
        subprocess.run(
            [
                "ffmpeg", "-i", file_path,
                "-vn", "-acodec", "libmp3lame", "-y",
                mp3_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    return AudioMeta(
        file_path=mp3_path,
        title=base_name,
        duration=0,
        platform="local",
        video_id=base_name,
    )
