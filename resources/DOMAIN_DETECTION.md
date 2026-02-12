# 领域自动检测规则

当收到视频转写内容后，按照以下流程判断该视频属于哪个专业领域。

## 检测流程

### 第一步：URL / 标题快速判断

检查视频 URL、标题、描述中是否包含明确的领域关键词：

| 领域 | URL / 标题关键词 |
|------|-----------------|
| Godot | godot, gdscript, godot engine |
| Unity | unity, unity3d, unity engine |
| Unreal | unreal, ue4, ue5, unreal engine |
| Blender | blender, blender3d |
| Pixel Art | pixel art, 像素画, aseprite, pixel animation |

如果标题中明确命中一个领域 → 直接输出该领域，跳过第二步。

### 第二步：转写内容关键指标扫描

读取 `full_text` 前 2000 字符，统计以下各领域独特指标的命中数量：

#### Godot 指标

| 指标 | 说明 |
|------|------|
| GDScript | Godot 专用脚本语言 |
| `@onready` | Godot 4.x 注解 |
| `@export` | Godot 4.x 导出变量 |
| CharacterBody2D / CharacterBody3D | Godot 4.x 物理角色节点 |
| KinematicBody2D | Godot 3.x 物理角色节点 |
| Node2D / Node3D | Godot 场景节点 |
| `.tscn` / `.tres` | Godot 场景/资源文件格式 |
| 场景树 / SceneTree | Godot 核心概念 |
| 检查器面板 / Inspector | 结合其他 Godot 指标 |
| `_ready()` / `_process()` / `_physics_process()` | Godot 生命周期函数 |

#### Unity 指标

| 指标 | 说明 |
|------|------|
| C# / csharp | Unity 主要脚本语言 |
| MonoBehaviour | Unity 脚本基类 |
| GameObject | Unity 核心对象 |
| Prefab | Unity 预制体 |
| Inspector / Hierarchy | Unity 编辑器面板 |
| URP / HDRP / Built-in | Unity 渲染管线 |
| `.unity` / `.prefab` | Unity 文件格式 |
| ScriptableObject | Unity 数据资产 |
| `Start()` / `Update()` / `Awake()` | Unity 生命周期函数 |
| AssetStore / Package Manager | Unity 包管理 |

#### Unreal Engine 指标

| 指标 | 说明 |
|------|------|
| Blueprint / 蓝图 | UE 可视化脚本 |
| Actor / Pawn / Character | UE 核心类 |
| `BeginPlay` / `Tick` | UE 生命周期函数 |
| Niagara | UE 粒子系统 |
| Nanite / Lumen | UE5 渲染技术 |
| MetaHuman | UE 数字人类 |
| `.uasset` / `.umap` | UE 文件格式 |
| Content Browser | UE 编辑器面板 |
| Details Panel / World Outliner | UE 编辑器面板 |
| UPROPERTY / UFUNCTION / UCLASS | UE C++ 宏 |

#### Blender 指标

| 指标 | 说明 |
|------|------|
| mesh / vertex / edge / face | 3D 建模基础元素 |
| modifier / 修改器 | Blender 修改器系统 |
| sculpt / 雕刻 | Blender 雕刻模式 |
| UV unwrap / UV 展开 | UV 编辑 |
| armature / 骨架 | Blender 绑定系统 |
| EEVEE / Cycles | Blender 渲染引擎 |
| `.blend` | Blender 文件格式 |
| Geometry Nodes / 几何节点 | Blender 程序化建模 |
| Shader Editor / 着色器编辑器 | Blender 材质编辑 |
| Edit Mode / Object Mode / Sculpt Mode | Blender 工作模式 |

#### Pixel Art 指标

| 指标 | 说明 |
|------|------|
| pixel art / 像素画 / 像素风 | 领域直接标识 |
| Aseprite | 主流像素画工具 |
| sprite sheet / 精灵图 | 像素动画输出格式 |
| palette / 调色板 / 色板 | 像素画核心概念 |
| dithering / 抖动 | 像素画技法 |
| anti-aliasing / 反锯齿 (像素语境) | 像素画技法 |
| tile / 瓦片 | 像素画瓦片设计 |
| 8-bit / 16-bit / retro | 复古风格标识 |
| Pyxel Edit / Piskel | 其他像素画工具 |
| sub-pixel animation / 亚像素动画 | 像素动画技法 |

## 置信规则

| 命中数量 | 置信度 | 处理 |
|---------|--------|------|
| 3+ 个独特指标命中同一领域 | 高置信 | 直接输出该领域 |
| 2 个指标命中 | 中置信 | 输出该领域，但在笔记开头注明"自动检测" |
| 多个领域均有命中 | 冲突 | 选择命中数最多的领域；若持平则询问用户 |
| 0-1 个指标命中 | 低置信 | 输出 unknown，询问用户 |

## 跨领域视频处理

当视频涉及多个领域时（如"Blender 建模导出到 Godot"）：
- 标题中提到更多次的领域优先
- 如果真正无法区分主次 → 询问用户选择主领域
- 笔记中可提及涉及的其他领域，但以主领域的 Prompt 结构为准

## 输出格式

检测结果必须为以下值之一：

- `godot`
- `unity`
- `unreal`
- `blender`
- `pixel-art`
- `unknown`
