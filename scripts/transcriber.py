"""Speech-to-text using faster-whisper (local, no API key needed)."""

import os
import logging
from pathlib import Path

# Fix OpenMP conflict on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from faster_whisper import WhisperModel

from models import TranscriptResult, TranscriptSegment

logger = logging.getLogger(__name__)

# Default model size — small balances speed and accuracy
DEFAULT_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")


def get_model(model_size: str = None) -> WhisperModel:
    """Load or download a faster-whisper model."""
    size = model_size or DEFAULT_MODEL_SIZE
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(model_dir, exist_ok=True)

    # Detect device
    device = "cpu"
    compute_type = "int8"
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "float16"
            logger.info("CUDA available, using GPU")
    except ImportError:
        pass

    logger.info(f"Loading whisper model: {size} on {device}")
    return WhisperModel(
        model_size_or_path=size,
        device=device,
        compute_type=compute_type,
        download_root=model_dir,
    )


def transcribe(file_path: str, model: WhisperModel = None) -> TranscriptResult:
    """Transcribe an audio file and return structured result."""
    if model is None:
        model = get_model()

    logger.info(f"Transcribing: {file_path}")
    segments_raw, info = model.transcribe(file_path)

    segments = []
    full_text = ""

    for seg in segments_raw:
        text = seg.text.strip()
        if text:
            full_text += text + " "
            segments.append(
                TranscriptSegment(start=seg.start, end=seg.end, text=text)
            )

    result = TranscriptResult(
        language=info.language,
        full_text=full_text.strip(),
        segments=segments,
    )
    logger.info(f"Transcription complete: {len(segments)} segments, language={info.language}")
    return result
