"""YouTube audio downloader using yt-dlp."""

import os
import json
import logging
import shutil
from typing import Optional

import yt_dlp

from models import AudioMeta, TranscriptResult, TranscriptSegment

logger = logging.getLogger(__name__)


def find_ffmpeg() -> Optional[str]:
    """Find FFmpeg executable path."""
    # Common Windows paths
    ffmpeg_paths = [
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
        r"C:\Users\32691\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
        "/usr/bin",
        "/usr/local/bin",
    ]
    for path in ffmpeg_paths:
        ffmpeg_path = os.path.join(path, "ffmpeg.exe" if os.name == "nt" else "ffmpeg")
        if os.path.exists(ffmpeg_path):
            return path
    # Try system PATH
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return os.path.dirname(ffmpeg)
    return None


def download_audio(url: str, output_dir: str) -> AudioMeta:
    """Download audio from a YouTube video and return metadata."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "%(id)s.%(ext)s")

    ffmpeg_location = find_ffmpeg()
    if ffmpeg_location:
        logger.info(f"Using FFmpeg from: {ffmpeg_location}")
    else:
        logger.warning("FFmpeg not found. Please install FFmpeg for audio extraction.")

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "quiet": True,
        "ffmpeg_location": ffmpeg_location,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info.get("id", "")
        title = info.get("title", "")
        duration = info.get("duration", 0)
        ext = info.get("ext", "m4a")
        audio_path = os.path.join(output_dir, f"{video_id}.{ext}")

    return AudioMeta(
        file_path=audio_path,
        title=title,
        duration=duration,
        platform="youtube",
        video_id=video_id,
    )


def download_subtitles(url: str, output_dir: str) -> Optional[TranscriptResult]:
    """Try to get YouTube subtitles. Returns None if unavailable."""
    os.makedirs(output_dir, exist_ok=True)
    langs = ["zh-Hans", "zh", "zh-CN", "zh-TW", "en", "en-US"]

    # Extract video id for file naming
    ydl_id_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_id_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_id = info.get("id", "unknown")

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
                detected_lang = next(iter(subtitles), None)
            if not detected_lang:
                return None

            subtitle_file = os.path.join(output_dir, f"{video_id}.{detected_lang}.json3")
            if not os.path.exists(subtitle_file):
                return None

            return _parse_json3(subtitle_file, detected_lang)
    except Exception as e:
        logger.warning(f"Failed to get YouTube subtitles: {e}")
        return None


def _parse_json3(path: str, language: str) -> Optional[TranscriptResult]:
    """Parse a json3 subtitle file into TranscriptResult."""
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
        raw={"source": "youtube_subtitle", "file": path},
    )
