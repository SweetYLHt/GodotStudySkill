# Godot Study

**Video Tutorial to Structured Learning Notes** - Automatically convert Godot game development video tutorials into well-organized study materials.

Supports **Bilibili**, **YouTube**, and **local video files**. Uses local AI transcription (no API key required).

## How It Works

```
Video URL / Local File
        |
        v
  [Download Audio]  ──>  [Try Platform Subtitles First]
        |                         |
        v                         v
  [Whisper Transcription]   [Parse Subtitles]
        |                         |
        +────────+────────────────+
                 |
                 v
       [Claude AI Analysis]
                 |
                 v
    [Structured Markdown Notes]
```

**Output includes:**
- Difficulty level auto-detection (beginner / intermediate / advanced)
- Godot version detection (3.x / 4.x)
- Knowledge point extraction with Godot API references
- Step-by-step editor operation paths
- Complete GDScript code blocks with annotations
- Scene tree structures and signal connection diagrams
- Common pitfalls and best practices
- Video timestamps for easy reference

## Quick Start

### Prerequisites

- Python 3.10+
- FFmpeg (for local video files)
- GPU with CUDA support (optional, for faster transcription)

### Installation

```bash
git clone https://github.com/SweetYLHt/BilinoteGodotStudy.git
cd BilinoteGodotStudy
pip install -r requirements.txt
```

### Usage

#### As a standalone tool

```bash
# From a Bilibili video
python scripts/main.py "https://www.bilibili.com/video/BV1xxxxx"

# From a YouTube video
python scripts/main.py "https://www.youtube.com/watch?v=xxxxx"

# From a local video file
python scripts/main.py "/path/to/tutorial.mp4"
```

The script outputs a transcript JSON file to `scripts/output/`. You can then use the transcript with your preferred LLM to generate structured notes using the prompt template in `resources/GODOT_PROMPT.md`.

#### As a Claude Code skill

This project is also a [Claude Code](https://claude.ai/claude-code) skill. After installing, use it directly in Claude Code:

```
/godot-study https://www.bilibili.com/video/BV1xxxxx
```

Claude will download, transcribe, analyze, and generate the complete learning document automatically.

To install as a Claude Code skill, copy the project to your Claude skills directory:

```bash
# Windows
cp -r . %USERPROFILE%\.claude\skills\godot-study

# macOS / Linux
cp -r . ~/.claude/skills/godot-study
```

## Project Structure

```
BilinoteGodotStudy/
├── README.md
├── LICENSE
├── requirements.txt
├── SKILL.md                  # Claude Code skill definition
├── resources/
│   └── GODOT_PROMPT.md       # Prompt template for learning note generation
├── scripts/
│   ├── main.py               # Main entry point
│   ├── models.py             # Data models (TranscriptSegment, AudioMeta, etc.)
│   ├── transcriber.py        # Whisper speech-to-text engine
│   └── downloaders/
│       ├── bilibili.py       # Bilibili video handler
│       ├── youtube.py        # YouTube video handler
│       └── local.py          # Local file handler
└── docs/
    └── godot-study/          # Generated learning notes output
```

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `WHISPER_MODEL_SIZE` | `base` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large-v3`) |

Larger models produce better transcriptions but require more VRAM/RAM and are slower.

## Prompt Template

The learning note generation is driven by `resources/GODOT_PROMPT.md`. It instructs the AI to:

1. **Auto-detect difficulty** - Analyzes keywords to classify as beginner/intermediate/advanced
2. **Detect Godot version** - Identifies 3.x vs 4.x from API patterns (`@onready` vs `onready`, etc.)
3. **Generate structured output** - Core ideas, knowledge points, operation paths, code architecture, signal connections, key takeaways

You can customize this prompt to adjust the output format or add domain-specific analysis rules.

## Example Output

See the `docs/godot-study/` directory for example generated learning notes.

## Dependencies

| Package | Purpose |
|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Video/audio downloading from Bilibili, YouTube, etc. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Local offline speech-to-text (CTranslate2-based) |

## License

[MIT](LICENSE)
