"""
godot-study-tool: Download video audio and transcribe to text.

Usage:
    python main.py <url-or-file-path>

Outputs transcript JSON path to stdout.
"""

import json
import os
import re
import sys
import logging
from dataclasses import asdict
from pathlib import Path

# Ensure scripts/ is on the import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import TranscriptResult

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def detect_platform(source: str) -> str:
    """Detect the platform from a URL or file path."""
    if os.path.exists(source):
        return "local"
    if "bilibili.com" in source or "b23.tv" in source:
        return "bilibili"
    if "youtube.com" in source or "youtu.be" in source:
        return "youtube"
    # Fallback: try as local path
    return "local"


def get_transcript(source: str) -> tuple:
    """
    Download audio and get transcript.
    Returns (TranscriptResult, title, platform).
    """
    platform = detect_platform(source)
    logger.info(f"Detected platform: {platform}")

    # Step 1: Try platform subtitles first
    transcript = None
    title = ""

    if platform == "bilibili":
        from downloaders import bilibili
        logger.info("Trying Bilibili subtitles...")
        transcript = bilibili.download_subtitles(source, OUTPUT_DIR)
        if transcript:
            logger.info("Got Bilibili subtitles, skipping audio download")
            # Still need title
            meta = bilibili.download_audio(source, OUTPUT_DIR)
            title = meta.title
            return transcript, title, platform
        logger.info("No subtitles, downloading audio...")
        meta = bilibili.download_audio(source, OUTPUT_DIR)
        title = meta.title

    elif platform == "youtube":
        from downloaders import youtube
        logger.info("Trying YouTube subtitles...")
        transcript = youtube.download_subtitles(source, OUTPUT_DIR)
        if transcript:
            logger.info("Got YouTube subtitles, skipping audio download")
            meta = youtube.download_audio(source, OUTPUT_DIR)
            title = meta.title
            return transcript, title, platform
        logger.info("No subtitles, downloading audio...")
        meta = youtube.download_audio(source, OUTPUT_DIR)
        title = meta.title

    elif platform == "local":
        from downloaders import local
        meta = local.download_audio(source, OUTPUT_DIR)
        title = meta.title

    else:
        raise ValueError(f"Unsupported platform: {platform}")

    # Step 2: Transcribe audio with faster-whisper
    from transcriber import transcribe
    logger.info(f"Transcribing audio: {meta.file_path}")
    transcript = transcribe(meta.file_path)

    return transcript, title, platform


def sanitize_filename(name: str) -> str:
    """Remove invalid filename characters."""
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    return name.strip()[:100]


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url-or-file-path>", file=sys.stderr)
        sys.exit(1)

    source = sys.argv[1]
    logger.info(f"Processing: {source}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    transcript, title, platform = get_transcript(source)

    # Save transcript JSON
    safe_title = sanitize_filename(title) if title else "untitled"
    output_file = os.path.join(OUTPUT_DIR, f"{safe_title}_transcript.json")

    data = {
        "title": title,
        "platform": platform,
        "source": source,
        "language": transcript.language,
        "full_text": transcript.full_text,
        "segments": [asdict(seg) for seg in transcript.segments],
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Print the output path to stdout for the skill to pick up
    print(output_file)
    logger.info(f"Transcript saved to: {output_file}")


if __name__ == "__main__":
    main()
