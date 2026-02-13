# GameDev Study — Video Tutorial to Learning Notes

Generate structured learning materials from game development video tutorials across multiple domains. Supports **Godot, Unity, Unreal Engine, Blender, and Pixel Art**.

## Trigger

`/gamedev-study <video-url-or-file-path> [--output <output-path>] [--domain <domain>]`

## Usage Flow

1. **Provide video URL** → Skill will ask for output directory
2. **Specify output path** → Transcript and notes will be saved there
3. **Domain auto-detection** → Or use `--domain` to specify manually

## Options

| Option | Description |
|--------|-------------|
| `<video-url-or-file-path>` | Video URL (Bilibili/YouTube) or local file path |
| `--output <path>` | (Optional) Output directory path. If not provided, skill will ask. |
| `--domain <domain>` | (Optional) Force domain: godot / unity / unreal / blender / pixel-art |

## Examples

```bash
# Basic usage - will ask for output path
/gamedev-study https://www.bilibili.com/video/BV1xxx

# With output path specified
/gamedev-study https://www.bilibili.com/video/BV1xxx --output D:\MyNotes

# With domain specified
/gamedev-study https://www.bilibili.com/video/BV1xxx --output D:\MyNotes --domain godot
```

## Output Directory Selection

When `--output` is not provided, the skill will ask:

```
请输入笔记输出路径（例如: D:\Godot学习笔记 或 ~/Documents/Notes）:
```

Supported paths:
- Absolute Windows path: `D:\Notes\Godot`
- Absolute Unix path: `/home/user/Notes`
- Relative path: `./notes` (relative to current working directory)

## URL Mode Flow

1. If `--output` not provided → ask user for output directory path
2. Run: `python <skill-dir>/scripts/main.py "<url>" --output "<output-dir>"` (timeout: 10 minutes)
3. Script outputs transcript JSON path to stdout
4. Read the transcript JSON file
5. Generate learning document in the specified output directory

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
4. Create output directory if not exists
5. Write result to `<output-path>/<sanitized-title>.md`

## Dependencies

Before first use, install Python dependencies:
```bash
pip install -r <skill-dir>/scripts/requirements.txt
```

## Notes

- Transcription uses local faster-whisper (no API key needed)
- Supports Bilibili, YouTube, and local video files
- Audio files are automatically deleted after transcription to save space
- Use `--output` to specify where notes should be saved
