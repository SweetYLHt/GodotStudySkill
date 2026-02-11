# Godot Study — Video Tutorial to Learning Notes

Generate structured Godot learning materials from video tutorials. Use when studying Godot game development from video content.

## Trigger

`/godot-study <video-url-or-file-path>`

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

## Generate Learning Document

1. Read `<skill-dir>/resources/GODOT_PROMPT.md` for the analysis prompt
2. Combine transcript content with the Godot prompt
3. Generate the learning document following the prompt structure
4. Create output directory `docs/godot-study/` if not exists
5. Write result to `docs/godot-study/<sanitized-title>.md`

## Dependencies

Before first use, install Python dependencies:
```bash
pip install -r <skill-dir>/scripts/requirements.txt
```

## Notes

- Transcription uses local faster-whisper (no API key needed)
- Supports Bilibili, YouTube, and local video files
- Claude performs the Godot-specific analysis directly (no external LLM call)
