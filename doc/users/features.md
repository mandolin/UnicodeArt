# 📚 功能详细说明

本文档详细介绍 UnicodeArt 的所有功能和参数。

---

## 🎯 核心功能概览

UnicodeArt 提供两大核心功能：

1. **图片转字符画** - 将任意图像转换为 ASCII/Unicode 字符艺术
2. **文本转字符画** - 将文本渲染为大型字符艺术（Banner）

---

## 📝 输入方式

### 1. 文本输入 (`--text` / `-t`)

**用途**: 将文本转换为大型字符画

**基本用法**:

```bash
python unicodeart.py -t "Hello" --font "path/to/font.ttf" --height 20
```

**多行文本**:

```bash
# 使用 \n 分隔
python unicodeart.py -t "Line1\nLine2\nLine3" --font "..." --height 15

# 从文件读取
python unicodeart.py -t "@myfile.txt" --font "..." --height 15
```

**必需参数**:

- `--font`: 字体文件路径（.ttf/.ttc）
- `--height`: 每行高度或总高度（取决于 `--height-mode`）

---

### 2. 图片输入 (`--image` / `-i`)

**用途**: 将图像转换为字符画

**基本用法**:

```bash
python unicodeart.py -i photo.jpg --height 30
```

**支持格式**: JPG, PNG, BMP, GIF, TIFF 等（OpenCV 支持的格式）

**可选参数**:

- `--width`: 指定输出宽度（保持宽高比时可省略）
- `--chars`: 自定义字符集

---

## ⚙️ 输出控制

### `--output` / `-o`

**用途**: 将结果保存到文件

**示例**:

```bash
python unicodeart.py -i photo.jpg --height 30 -o result.txt
```

**默认行为**: 不指定时输出到终端（stdout）

---

### `--height`

**用途**: 控制输出高度

**含义取决于 `--height-mode`**:

#### 模式 1: `line`（默认）

- `--height` 表示**每行字符画的高度**
- 总高度 = 每行高度 × 行数 + 行间距
- 适合需要精确控制单行大小的场景

```bash
# 每行 20 像素高，共 3 行文本
python unicodeart.py -t "A\nB\nC" --height 20 --height-mode line
```

#### 模式 2: `total`

- `--height` 表示**整体输出的总高度**
- 自动计算每行高度
- 适合固定显示区域的场景

```bash
# 总高度 60 像素，自动分配给 3 行
python unicodeart.py -t "A\nB\nC" --height 60 --height-mode total
```

---

### `--width`

**用途**: 控制输出宽度

**行为**:

- 仅适用于图片模式
- 文本模式忽略此参数
- 不指定时根据图片宽高比自动计算

```bash
# 固定宽度 80 字符
python unicodeart.py -i photo.jpg --height 30 --width 80
```

---

## 🔤 字符集配置

### `--chars`

**用途**: 自定义用于匹配的字符集

**默认值**: `" .:-=+*#%@"`（从暗到亮）

**示例**:

```bash
# 简化字符集（低细节）
python unicodeart.py -i photo.jpg --chars " ░█"

# 丰富字符集（高细节）
python unicodeart.py -i photo.jpg --chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# 块状字符（适合终端）
python unicodeart.py -i photo.jpg --chars " ░▒▓█"
```

**选择建议**:

- **简单图形**: 3-5 个字符
- **照片**: 8-12 个字符
- **高精度**: 15+ 个字符

---

### `--wide-chars`

**用途**: 指定宽字符集（中文、日文等）

**默认值**: 自动识别 Unicode 宽字符

**示例**:

```bash
# 自定义宽字符集
python unicodeart.py -i photo.jpg --wide-chars "一二三四五六七八九十"
```

---

## 🎨 字体与渲染

### `--font`

**用途**: 指定字体文件路径

**支持格式**: .ttf, .ttc, .otf

**Windows 常用字体**:

```bash
# 宋体
--font "C:\Windows\Fonts\SimSun.ttc"

# 微软雅黑
--font "C:\Windows\Fonts\MSYH.TTC"

# Consolas（等宽英文）
--font "C:\Windows\Fonts\consola.ttf"
```

**macOS 常用字体**:

```bash
# 苹方
--font "/Library/Fonts/PingFang.ttc"

# Helvetica
--font "/System/Library/Fonts/Helvetica.ttc"
```

---

### `--font-style`

**用途**: 设置字体样式

**可选值**:

- `normal`（默认）
- `bold`
- `italic`
- `bold-italic`

**示例**:

```bash
python unicodeart.py -t "Bold Text" --font "..." --font-style bold --height 20
```

**注意**: 字体文件必须包含对应样式，否则回退到 normal

---

### `--font-reduce`

**用途**: 字体大小缩减量（像素）

**默认值**: `0`

**作用**: 调整字符在矩阵中的填充程度

**示例**:

```bash
# 减少字体大小，增加留白
python unicodeart.py -t "Text" --font "..." --font-reduce 2 --height 20

# 增大字体，减少留白
python unicodeart.py -t "Text" --font "..." --font-reduce -1 --height 20
```

**推荐值**:

- 正常: `0`
- 紧凑: `-1` 到 `-2`
- 宽松: `1` 到 `3`

---

## 📐 采样与匹配

### `--matrix` / `-m`

**用途**: 采样矩阵大小

**默认值**: `6`

**含义**: 每个字符用 `matrix × matrix` 的灰度矩阵表示

**影响**:

- **较大值** (8-10): 更精细，但速度慢
- **较小值** (4-5): 更快，但细节少

**示例**:

```bash
# 高精度
python unicodeart.py -i photo.jpg --matrix 8 --height 30

# 快速预览
python unicodeart.py -i photo.jpg --matrix 4 --height 30
```

**性能对比**:

- `matrix=4`: 最快，适合实时处理
- `matrix=6`: 平衡（推荐）
- `matrix=8`: 高质量，适合打印

---

### `--ratio` / `-r`

**用途**: 字符高度与宽度的比例

**默认值**: `2.0`（标准混合等宽字体的正确比例）

**重要说明**:
- `--ratio=2.0` 是**通用标准**，适用于所有使用混合等宽字体显示的环境
- 在 VSCode、终端、浏览器等使用等宽字体（英文字符:中文字符 = 1:2）的环境中，**无需调整**
- 只有在特殊显示环境（非等宽字体）下才需要微调

**何时需要调整**:
- 您的编辑器/终端使用的**显示字体**不是混合等宽字体
- 观察到字符画整体变形（过宽或过窄）

**示例**:

```bash
# 标准用法（推荐，适用于绝大多数场景）
python unicodeart.py -t "Hello" --font "SimSun.ttc" --ratio 2.0 --height 20

# 特殊情况：如果显示环境不是等宽字体，可尝试调整
python unicodeart.py -t "Hello" --font "SimSun.ttc" --ratio 1.5 --height 20
```

---

### `--interpolation`

**用途**: 图像缩放插值算法

**可选值**:

- `nearest`: 最近邻（最快，锯齿明显）
- `bilinear`: 双线性（默认，平衡）
- `bicubic`: 双三次（较慢，平滑）
- `lanczos`: Lanczos（最慢，最高质量）

**示例**:

```bash
# 快速处理
python unicodeart.py -i photo.jpg --interpolation nearest --height 30

# 高质量
python unicodeart.py -i photo.jpg --interpolation lanczos --height 30
```

**性能排序**: nearest > bilinear > bicubic > lanczos
**质量排序**: lanczos > bicubic > bilinear > nearest

---

## 🔀 宽字符处理

### `--wide-char-ratio`

**用途**: 宽字符匹配得分权重

**默认值**: `2.0`

**含义**: 宽字符得分需小于普通字符得分的 `wide_char_ratio` 倍才优先使用

**调整场景**:

- 宽字符识别过多: 增大（如 `3.0`）
- 宽字符识别过少: 减小（如 `1.5`）

**示例**:

```bash
# 优先使用宽字符
python unicodeart.py -i photo.jpg --wide-char-ratio 1.5

# 谨慎使用宽字符
python unicodeart.py -i photo.jpg --wide-char-ratio 3.0
```

---

## 📏 行间距控制

### `--line-spacing`

**用途**: 多行文本的行间距（字符画行数）

**默认值**: `0`

**仅在多行文本时生效**

**示例**:

```bash
# 无间距
python unicodeart.py -t "A\nB\nC" --line-spacing 0 --height 15

# 1 行间距
python unicodeart.py -t "A\nB\nC" --line-spacing 1 --height 15

# 2 行间距
python unicodeart.py -t "A\nB\nC" --line-spacing 2 --height 15
```

**视觉效果**:

```
# line-spacing=0
AAAA
BBBB
CCCC

# line-spacing=1
AAAA

BBBB

CCCC
```

---

## 🔄 其他选项

### `--invert` / `-v`

**用途**: 反转颜色（黑白互换）

**示例**:

```bash
python unicodeart.py -i photo.jpg --invert --height 30
```

**适用场景**:

- 深色背景终端
- 特殊艺术效果

---

### `--debug` / `-d`

**用途**: 调试模式，输出详细日志

**可选标签**（逗号分隔）:

- `sampling`: 采样过程
- `matching`: 匹配过程
- `all`: 全部信息

**示例**:

```bash
python unicodeart.py -i photo.jpg --debug sampling,matching --height 10
```

---

### `--print` / `-p`

**用途**: 控制 print 输出

**可选值**:

- `spec`（默认）: 仅输出字符画
- `all`: 输出所有调试信息
- `no`: 不执行 print（适合外部调用）

**示例**:

```bash
# 脚本调用时禁用输出
python unicodeart.py -i photo.jpg --print no -o result.txt
```

---

## 🎯 参数组合推荐

### 场景 1: 终端快速预览

```bash
python unicodeart.py -i photo.jpg \
  --height 20 \
  --matrix 4 \
  --interpolation nearest \
  --chars " ░▒▓█"
```

### 场景 2: 社交媒体分享

```bash
python unicodeart.py -i photo.jpg \
  --height 50 \
  --matrix 6 \
  --interpolation bilinear \
  --chars " .:-=+*#%@" \
  -o output.txt
```

### 场景 3: 高质量打印

```bash
python unicodeart.py -i photo.jpg \
  --height 100 \
  --matrix 8 \
  --interpolation lanczos \
  --chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" \
  -o output.txt
```

### 场景 4: 中文文本 Banner

```bash
python unicodeart.py -t "你好世界" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 20 \
  --matrix 6 \
  --ratio 1.2 \
  --font-reduce 0
```

---

## ❓ 常见问题

**Q: 如何选择合适的 `--height`？**
A: 终端显示用 20-40，社交媒体用 50-100，打印用 100+

**Q: 为什么中文字符变形？**
A: 尝试调整 `--ratio`（宋体推荐 2）和 `--matrix`（推荐 6）

**Q: 输出太慢怎么办？**
A: 减小 `--height`、`--matrix`，使用 `nearest` 插值

**Q: 如何获得更细腻的 effect？**
A: 增加 `--matrix`（8-10），使用更多字符的 `--chars`

---

## 📖 相关文档

- 🚀 [快速入门](quick-start.md)
- ❓ [常见问题](faq.md)
- 📖 [使用示例](examples/)

---

*最后更新: 2026-06-09*
