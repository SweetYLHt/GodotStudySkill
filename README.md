# GameStudySkill

[English](README_EN.md)

**视频教程转结构化学习笔记** — 自动将游戏开发视频教程转换为条理清晰的学习资料。

支持 **Godot、Unity、Unreal Engine、Blender 和像素画** 领域，可自动检测视频所属领域。

支持 **Bilibili**、**YouTube** 和 **本地视频文件**。使用本地 AI 语音转文字（无需 API Key）。

## 支持的领域

| 领域 | 说明 | Prompt 文件 |
|------|------|-------------|
| Godot | GDScript、场景树、节点系统 | `GODOT_PROMPT.md` |
| Unity | C#、MonoBehaviour、组件系统 | `UNITY_PROMPT.md` |
| Unreal Engine | Blueprint、C++、Actor/Component | `UNREAL_PROMPT.md` |
| Blender | 3D 建模、修改器、节点编辑器 | `BLENDER_PROMPT.md` |
| 像素画 | Aseprite、抖动、调色板设计 | `PIXEL_ART_PROMPT.md` |

## 工作流程

```
视频链接 / 本地文件
        |
        v
  [下载音频]  ──>  [优先尝试平台字幕]
        |                   |
        v                   v
  [Whisper 语音转文字]   [解析字幕]
        |                   |
        +────────+──────────+
                 |
                 v
         [领域检测]  ──>  自动检测 或 --domain 手动指定
                 |
                 v
       [加载领域 Prompt]  ──>  GODOT / UNITY / UNREAL / BLENDER / PIXEL_ART
                 |
                 v
        [Claude AI 分析]
                 |
                 v
       [结构化 Markdown 笔记]
```

**输出内容（按领域定制）：**
- 难度等级自动检测（入门 / 中级 / 高级）
- 版本/工具识别（如 Godot 4.x、Unity 2022 LTS、UE5、Blender 4.x、Aseprite）
- 知识点提取，附带领域专属 API/工具参考
- 分步骤编辑器/工具操作路径
- 完整代码块或技术拆解，附注释说明
- 架构图示（场景树、节点图、修改器堆栈、调色板图表）
- 常见陷阱与最佳实践
- 视频时间戳，方便回看

## 快速开始

### 前置要求

- Python 3.10+
- FFmpeg（处理本地视频文件时需要）
- 支持 CUDA 的 GPU（可选，加速语音转文字）

### 安装

```bash
git clone https://github.com/SweetYLHt/GameStudySkill.git
cd GameStudySkill
pip install -r requirements.txt
```

### 使用方法

#### 作为独立工具使用

```bash
# Bilibili 视频
python scripts/main.py "https://www.bilibili.com/video/BV1xxxxx"

# YouTube 视频
python scripts/main.py "https://www.youtube.com/watch?v=xxxxx"

# 本地视频文件
python scripts/main.py "/path/to/tutorial.mp4"

# 自定义输出目录
python scripts/main.py "video.mp4" -o /path/to/notes

# 保留音频文件（默认转录后自动删除以节省空间）
python scripts/main.py "video.mp4" --keep-audio
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `-o, --output DIR` | 指定输出目录（默认: `./output`） |
| `--keep-audio` | 转录完成后保留音频文件（默认: 自动删除） |
| `-h, --help` | 显示帮助信息 |

脚本会将转录结果以 JSON 格式输出到指定目录。

#### 作为 Claude Code 技能使用

本项目同时也是一个 [Claude Code](https://claude.ai/claude-code) 技能。安装后可以直接在 Claude Code 中使用：

```
# 自动检测领域
/gamedev-study https://www.bilibili.com/video/BV1xxxxx

# 手动指定领域
/gamedev-study https://www.youtube.com/watch?v=xxxxx --domain unity
```

Claude 会自动完成下载、转录、领域检测并生成完整的学习文档。

安装为 Claude Code 技能，将项目复制到技能目录即可：

```bash
# Windows
cp -r . %USERPROFILE%\.claude\skills\gamedev-study

# macOS / Linux
cp -r . ~/.claude/skills/gamedev-study
```

## 项目结构

```
GameStudySkill/
├── README.md                      # 中文说明
├── README_EN.md                   # English README
├── LICENSE
├── requirements.txt
├── SKILL.md                       # Claude Code 技能定义（多领域）
├── resources/
│   ├── DOMAIN_DETECTION.md        # 自动领域检测规则
│   ├── GODOT_PROMPT.md            # Godot 学习笔记 Prompt
│   ├── UNITY_PROMPT.md            # Unity 学习笔记 Prompt
│   ├── UNREAL_PROMPT.md           # Unreal Engine 学习笔记 Prompt
│   ├── BLENDER_PROMPT.md          # Blender 学习笔记 Prompt
│   └── PIXEL_ART_PROMPT.md        # 像素画学习笔记 Prompt
├── scripts/
│   ├── main.py                    # 主入口
│   ├── models.py                  # 数据模型（TranscriptSegment、AudioMeta 等）
│   ├── transcriber.py             # Whisper 语音转文字引擎
│   └── downloaders/
│       ├── bilibili.py            # Bilibili 视频处理
│       ├── youtube.py             # YouTube 视频处理
│       └── local.py               # 本地文件处理
└── docs/
    ├── godot-study/               # Godot 学习笔记输出
    ├── unity-study/               # Unity 学习笔记输出
    ├── unreal-study/              # Unreal Engine 学习笔记输出
    ├── blender-study/             # Blender 学习笔记输出
    └── pixel-art-study/           # 像素画学习笔记输出
```

## 配置

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `WHISPER_MODEL_SIZE` | `base` | Whisper 模型大小（`tiny`、`base`、`small`、`medium`、`large-v3`） |

更大的模型转录质量更好，但需要更多显存/内存，速度也更慢。

## 领域检测

系统通过以下方式自动检测视频所属领域：
1. **URL / 标题关键词** — 针对明显匹配的快速路径
2. **转录内容** — 扫描前 2000 个字符中的领域特征词

检测规则定义在 `resources/DOMAIN_DETECTION.md` 中。当自动检测失败时，系统会询问用户选择。

也可以通过 `--domain` 参数直接指定领域，跳过自动检测。

## Prompt 模板

每个领域在 `resources/` 目录下都有独立的 Prompt 模板，所有模板共享统一结构：

1. **自动判断难度** — 根据内容分析判定：入门 / 中级 / 高级
2. **版本/工具识别** — 识别具体版本、工具或配置
3. **生成结构化输出** — 核心思路、知识点、操作路径、架构图、关键要点

你可以自定义任何 Prompt 来调整输出格式或添加领域专属的分析规则。

## 示例输出

参见 `docs/godot-study/` 目录中的示例学习笔记。

## 依赖

| 包 | 用途 |
|----|------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 从 Bilibili、YouTube 等平台下载视频/音频 |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 本地离线语音转文字（基于 CTranslate2） |

## 许可证

[MIT](LICENSE)
