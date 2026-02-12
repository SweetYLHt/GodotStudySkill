# GameStudySkill

**Video Tutorial to Structured Learning Notes** — Automatically convert game development video tutorials into well-organized study materials.

Supports **Godot, Unity, Unreal Engine, Blender, and Pixel Art** with automatic domain detection.

Supports **Bilibili**, **YouTube**, and **local video files**. Uses local AI transcription (no API key required).

## Supported Domains

| Domain | Description | Prompt |
|--------|------------|--------|
| Godot | GDScript, scene tree, node system | `GODOT_PROMPT.md` |
| Unity | C#, MonoBehaviour, component system | `UNITY_PROMPT.md` |
| Unreal Engine | Blueprint, C++, Actor/Component | `UNREAL_PROMPT.md` |
| Blender | 3D modeling, modifiers, node editors | `BLENDER_PROMPT.md` |
| Pixel Art | Aseprite, dithering, palette design | `PIXEL_ART_PROMPT.md` |

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
       [Domain Detection]  ──>  auto-detect or --domain flag
                 |
                 v
       [Load Domain Prompt]  ──>  GODOT / UNITY / UNREAL / BLENDER / PIXEL_ART
                 |
                 v
       [Claude AI Analysis]
                 |
                 v
    [Structured Markdown Notes]
```

**Output includes (per domain):**
- Difficulty level auto-detection (beginner / intermediate / advanced)
- Version/tool detection (e.g., Godot 4.x, Unity 2022 LTS, UE5, Blender 4.x, Aseprite)
- Knowledge point extraction with domain-specific API/tool references
- Step-by-step editor/tool operation paths
- Complete code blocks or technique breakdowns with annotations
- Architecture diagrams (scene trees, node graphs, modifier stacks, palette charts)
- Common pitfalls and best practices
- Video timestamps for easy reference

## Quick Start

### Prerequisites

- Python 3.10+
- FFmpeg (for local video files)
- GPU with CUDA support (optional, for faster transcription)

### Installation

```bash
git clone https://github.com/SweetYLHt/GameStudySkill.git
cd GameStudySkill
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

The script outputs a transcript JSON file to `scripts/output/`. You can then use the transcript with your preferred LLM to generate structured notes using the appropriate prompt template from `resources/`.

#### As a Claude Code skill

This project is also a [Claude Code](https://claude.ai/claude-code) skill. After installing, use it directly in Claude Code:

```
# Auto-detect domain
/gamedev-study https://www.bilibili.com/video/BV1xxxxx

# Specify domain manually
/gamedev-study https://www.youtube.com/watch?v=xxxxx --domain unity
```

Claude will download, transcribe, detect the domain, and generate the complete learning document automatically.

To install as a Claude Code skill, copy the project to your Claude skills directory:

```bash
# Windows
cp -r . %USERPROFILE%\.claude\skills\gamedev-study

# macOS / Linux
cp -r . ~/.claude/skills/gamedev-study
```

## Project Structure

```
GameStudySkill/
├── README.md
├── LICENSE
├── requirements.txt
├── SKILL.md                       # Claude Code skill definition (multi-domain)
├── resources/
│   ├── DOMAIN_DETECTION.md        # Auto domain detection rules
│   ├── GODOT_PROMPT.md            # Godot learning note prompt
│   ├── UNITY_PROMPT.md            # Unity learning note prompt
│   ├── UNREAL_PROMPT.md           # Unreal Engine learning note prompt
│   ├── BLENDER_PROMPT.md          # Blender learning note prompt
│   └── PIXEL_ART_PROMPT.md        # Pixel Art learning note prompt
├── scripts/
│   ├── main.py                    # Main entry point
│   ├── models.py                  # Data models (TranscriptSegment, AudioMeta, etc.)
│   ├── transcriber.py             # Whisper speech-to-text engine
│   └── downloaders/
│       ├── bilibili.py            # Bilibili video handler
│       ├── youtube.py             # YouTube video handler
│       └── local.py               # Local file handler
└── docs/
    ├── godot-study/               # Godot learning notes output
    ├── unity-study/               # Unity learning notes output
    ├── unreal-study/              # Unreal Engine learning notes output
    ├── blender-study/             # Blender learning notes output
    └── pixel-art-study/           # Pixel Art learning notes output
```

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `WHISPER_MODEL_SIZE` | `base` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large-v3`) |

Larger models produce better transcriptions but require more VRAM/RAM and are slower.

## Domain Detection

The system automatically detects the video's domain by analyzing:
1. **URL / Title keywords** — fast path for obvious matches
2. **Transcript content** — scans the first 2000 characters for domain-specific indicators

Detection rules are defined in `resources/DOMAIN_DETECTION.md`. When auto-detection fails, the system asks the user to choose.

You can bypass detection entirely with the `--domain` flag.

## Prompt Templates

Each domain has its own prompt template in `resources/`. All prompts share a common structure:

1. **Auto-detect difficulty** — Beginner / Intermediate / Advanced based on content analysis
2. **Version/tool detection** — Identifies specific versions, tools, or configurations
3. **Generate structured output** — Core ideas, knowledge points, operation paths, architecture, key takeaways

You can customize any prompt to adjust the output format or add domain-specific analysis rules.

## Example Output

See the `docs/godot-study/` directory for example generated learning notes.

## Dependencies

| Package | Purpose |
|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Video/audio downloading from Bilibili, YouTube, etc. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Local offline speech-to-text (CTranslate2-based) |

## License

[MIT](LICENSE)
