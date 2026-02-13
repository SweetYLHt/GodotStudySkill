"""
godot-study-tool: Download video audio and transcribe to text.

Usage:
    python main.py <url-or-file-path> [options]

Options:
    -o, --output DIR     Output directory for transcripts (default: ./output)
    --keep-audio         Keep audio files after transcription (default: delete)
    -h, --help           Show this help message

Outputs transcript JSON path to stdout.
"""

import json
import os
import re
import sys
import argparse
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


def cleanup_audio(file_path: str) -> None:
    """Remove audio file after transcription to save disk space."""
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            logger.info(f"Cleaned up audio file: {file_path}")
        except OSError as e:
            logger.warning(f"Failed to clean up audio file: {e}")


def get_transcript(source: str, output_dir: str, keep_audio: bool = False) -> tuple:
    """
    Download audio and get transcript.
    Returns (TranscriptResult, title, platform, audio_file_path).
    """
    platform = detect_platform(source)
    logger.info(f"Detected platform: {platform}")

    audio_file_path = ""

    # Step 1: Try platform subtitles first
    transcript = None
    title = ""

    if platform == "bilibili":
        from downloaders import bilibili
        logger.info("Trying Bilibili subtitles...")
        transcript = bilibili.download_subtitles(source, output_dir)
        if transcript:
            logger.info("Got Bilibili subtitles, skipping audio download")
            # Still need title
            meta = bilibili.download_audio(source, output_dir)
            title = meta.title
            audio_file_path = meta.file_path
            return transcript, title, platform, audio_file_path
        logger.info("No subtitles, downloading audio...")
        meta = bilibili.download_audio(source, output_dir)
        title = meta.title
        audio_file_path = meta.file_path

    elif platform == "youtube":
        from downloaders import youtube
        logger.info("Trying YouTube subtitles...")
        transcript = youtube.download_subtitles(source, output_dir)
        if transcript:
            logger.info("Got YouTube subtitles, skipping audio download")
            meta = youtube.download_audio(source, output_dir)
            title = meta.title
            audio_file_path = meta.file_path
            return transcript, title, platform, audio_file_path
        logger.info("No subtitles, downloading audio...")
        meta = youtube.download_audio(source, output_dir)
        title = meta.title
        audio_file_path = meta.file_path

    elif platform == "local":
        from downloaders import local
        meta = local.download_audio(source, output_dir)
        title = meta.title
        audio_file_path = meta.file_path

    else:
        raise ValueError(f"Unsupported platform: {platform}")

    # Step 2: Transcribe audio with faster-whisper
    from transcriber import transcribe
    logger.info(f"Transcribing audio: {audio_file_path}")
    transcript = transcribe(audio_file_path)

    # Clean up audio file if not keeping it
    if not keep_audio:
        cleanup_audio(audio_file_path)

    return transcript, title, platform, ""


def sanitize_filename(name: str) -> str:
    """Remove invalid filename characters."""
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    return name.strip()[:100]


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert video tutorials to structured learning notes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python main.py "https://bilibili.com/video/BVxxx"

  # Custom output directory
  python main.py "video.mp4" -o /path/to/notes

  # Keep audio files after transcription
  python main.py "https://youtube.com/watch?v=xxx" --keep-audio
        """,
    )
    parser.add_argument(
        "source",
        help="Video URL or local file path",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory for transcripts (default: ./output)",
        default="./output",
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep audio files after transcription (default: delete to save space)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    source = args.source
    output_dir = os.path.abspath(args.output)
    keep_audio = args.keep_audio

    logger.info(f"Processing: {source}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Keep audio files: {keep_audio}")

    os.makedirs(output_dir, exist_ok=True)

    transcript, title, platform, _ = get_transcript(source, output_dir, keep_audio)

    # Save transcript JSON
    safe_title = sanitize_filename(title) if title else "untitled"
    output_file = os.path.join(output_dir, f"{safe_title}_transcript.json")

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
