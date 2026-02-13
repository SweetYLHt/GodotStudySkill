"""Bilibili audio downloader using yt-dlp."""

import os
import re
import logging
from pathlib import Path
from typing import Optional

import yt_dlp

from models import AudioMeta, TranscriptResult, TranscriptSegment

logger = logging.getLogger(__name__)

# FFmpeg location - auto-detect common paths
FFMPEG_PATHS = [
    r"C:\Program Files\ffmpeg\bin",
    r"C:\Program Files (x86)\ffmpeg\bin",
    r"C:\Users\32691\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
    "/usr/bin",
    "/usr/local/bin",
]

def find_ffmpeg() -> Optional[str]:
    """Find FFmpeg executable path."""
    for path in FFMPEG_PATHS:
        ffmpeg_path = os.path.join(path, "ffmpeg.exe" if os.name == "nt" else "ffmpeg")
        if os.path.exists(ffmpeg_path):
            return path
    # Try system PATH
    import shutil
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return os.path.dirname(ffmpeg)
    return None


def extract_video_id(url: str) -> str:
    """Extract BV id from a Bilibili URL."""
    match = re.search(r"(BV[\w]+)", url)
    if match:
        return match.group(1)
    match = re.search(r"av(\d+)", url)
    if match:
        return f"av{match.group(1)}"
    return url.split("/")[-1].split("?")[0]


def download_audio(url: str, output_dir: str) -> AudioMeta:
    """Download audio from a Bilibili video and return metadata."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "%(id)s.%(ext)s")

    # Get FFmpeg location
    ffmpeg_location = find_ffmpeg()
    if ffmpeg_location:
        logger.info(f"Using FFmpeg from: {ffmpeg_location}")
    else:
        logger.warning("FFmpeg not found. Please install FFmpeg for audio extraction.")

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "64",
            }
        ],
        "noplaylist": True,
        "quiet": True,
        "ffmpeg_location": ffmpeg_location,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info.get("id", "")
        title = info.get("title", "")
        duration = info.get("duration", 0)
        audio_path = os.path.join(output_dir, f"{video_id}.mp3")

    return AudioMeta(
        file_path=audio_path,
        title=title,
        duration=duration,
        platform="bilibili",
        video_id=video_id,
    )


def download_subtitles(url: str, output_dir: str) -> Optional[TranscriptResult]:
    """Try to get Bilibili subtitles. Returns None if unavailable."""
    os.makedirs(output_dir, exist_ok=True)
    video_id = extract_video_id(url)
    langs = ["zh-Hans", "zh", "zh-CN", "ai-zh", "en", "en-US"]

    ydl_opts = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": langs,
        "subtitlesformat": "json3",
        "skip_download": True,
        "outtmpl": os.path.join(output_dir, f"{video_id}.%(ext)s"),
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            subtitles = info.get("requested_subtitles") or {}
            if not subtitles:
                return None

            detected_lang = None
            for lang in langs:
                if lang in subtitles:
                    detected_lang = lang
                    break
            if not detected_lang:
                for lang in subtitles:
                    if lang != "danmaku":
                        detected_lang = lang
                        break
            if not detected_lang:
                return None

            subtitle_file = os.path.join(output_dir, f"{video_id}.{detected_lang}.json3")
            if not os.path.exists(subtitle_file):
                return None

            return _parse_json3(subtitle_file, detected_lang)
    except Exception as e:
        logger.warning(f"Failed to get Bilibili subtitles: {e}")
        return None


def _parse_json3(path: str, language: str) -> Optional[TranscriptResult]:
    """Parse a json3 subtitle file into TranscriptResult."""
    import json

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = []
    for event in data.get("events", []):
        start_ms = event.get("tStartMs", 0)
        duration_ms = event.get("dDurationMs", 0)
        segs = event.get("segs", [])
        text = "".join(seg.get("utf8", "") for seg in segs).strip()
        if text:
            segments.append(
                TranscriptSegment(
                    start=start_ms / 1000.0,
                    end=(start_ms + duration_ms) / 1000.0,
                    text=text,
                )
            )

    if not segments:
        return None

    full_text = " ".join(seg.text for seg in segments)
    return TranscriptResult(
        language=language,
        full_text=full_text,
        segments=segments,
        raw={"source": "bilibili_subtitle", "file": path},
    )
