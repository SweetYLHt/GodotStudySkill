# GameDev Study — Video Tutorial to Learning Notes

Generate structured learning materials from game development video tutorials across multiple domains. Supports **Godot, Unity, Unreal Engine, Blender, and Pixel Art**.

## Trigger

`/gamedev-study <video-url-or-file-path> [--domain <domain>]`

## Supported Domains

| Domain | Prompt File | Output Directory |
|--------|------------|------------------|
| `godot` | `GODOT_PROMPT.md` | `docs/godot-study/` |
| `unity` | `UNITY_PROMPT.md` | `docs/unity-study/` |
| `unreal` | `UNREAL_PROMPT.md` | `docs/unreal-study/` |
| `blender` | `BLENDER_PROMPT.md` | `docs/blender-study/` |
| `pixel-art` | `PIXEL_ART_PROMPT.md` | `docs/pixel-art-study/` |

## Input Detection

- Starts with `http://` or `https://` → **URL mode**: download + transcribe via `scripts/main.py`
- Ends with `.json` or `.md` → **File mode**: read existing transcript or notes directly
- Otherwise → treat as file path

## URL Mode Flow

1. Run: `python <skill-dir>/scripts/main.py "<url>"` (timeout: 10 minutes)
2. Script outputs transcript JSON path to stdout
3. Read the transcript JSON file

## File Mode Flow

1. If `.json`: read as transcript (expects `{full_text, segments}` format)
2. If `.md`: read as existing notes text

## Domain Detection

After obtaining the transcript content, determine which domain the video belongs to:

1. **If `--domain` argument is provided** → use it directly, skip detection
2. **Otherwise** → read `<skill-dir>/resources/DOMAIN_DETECTION.md` and follow its rules:
   - First check URL / title for explicit domain keywords
   - Then scan the first 2000 characters of `full_text` for domain-specific indicators
   - If 3+ indicators match a single domain → use that domain (high confidence)
   - If indicators are ambiguous or no clear match → ask the user to choose:
     "无法自动判断该视频的领域，请选择: godot / unity / unreal / blender / pixel-art"

## Generate Learning Document

1. Based on the detected domain, read the corresponding prompt file from `<skill-dir>/resources/`:
   - `godot` → `GODOT_PROMPT.md`
   - `unity` → `UNITY_PROMPT.md`
   - `unreal` → `UNREAL_PROMPT.md`
   - `blender` → `BLENDER_PROMPT.md`
   - `pixel-art` → `PIXEL_ART_PROMPT.md`
2. Combine transcript content with the domain prompt
3. Generate the learning document following the prompt structure
4. Create output directory `docs/<domain>-study/` if not exists
5. Write result to `docs/<domain>-study/<sanitized-title>.md`

## Dependencies

Before first use, install Python dependencies:
```bash
pip install -r <skill-dir>/scripts/requirements.txt
```

## Notes

- Transcription uses local faster-whisper (no API key needed)
- Supports Bilibili, YouTube, and local video files
- Claude performs the domain-specific analysis directly (no external LLM call)
- Domain detection is automatic but can be overridden with `--domain`
