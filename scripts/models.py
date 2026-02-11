from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass
class TranscriptResult:
    language: Optional[str]
    full_text: str
    segments: List[TranscriptSegment]
    raw: Optional[dict] = None


@dataclass
class AudioMeta:
    file_path: str
    title: str
    duration: float
    platform: str
    video_id: str
