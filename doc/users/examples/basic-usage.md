# 📖 基础用法示例

本文档提供 UnicodeArt 的基础使用示例，适合初学者快速上手。

---

## 🎯 示例 1: 最简单的文本转换

**场景**: 将短文本转换为字符画

``bash
python unicodeart.py -t "Hi" --font "C:\Windows\Fonts\SimSun.ttc" --height 15
```

**运行效果**:
终端会输出由字符组成的大型 "Hi" 字样，具体样式取决于您使用的字体和终端显示设置。

**要点**:
- 使用 `-t` 指定文本
- 必须提供 `--font`（字体路径）
- `--height` 控制大小

---

## 🎯 示例 2: 图片转字符画（默认配置）

**场景**: 快速将照片转换为字符画

```bash
python unicodeart.py -i photo.jpg --height 30
```

**说明**:
- 自动使用默认字符集 `" .:-=+*#%@"`
- 自动计算宽度（保持宽高比）
- 输出到终端

**提示**: 适合快速预览效果

---

## 🎯 示例 3: 保存到文件

**场景**: 生成字符画并保存

```bash
python unicodeart.py -i landscape.jpg --height 40 -o art.txt
```

**查看结果**:
```bash
# Windows
type art.txt

# Linux/macOS
cat art.txt
```

**用途**: 
- 分享到社交媒体
- 嵌入文档
- 打印输出

---

## 🎯 示例 4: 自定义字符集

**场景**: 使用特定字符风格

### 块状风格（适合终端）
```bash
python unicodeart.py -i portrait.jpg \
  --height 30 \
  --chars " ░▒▓█"
```

### ASCII 艺术风格
```bash
python unicodeart.py -i city.jpg \
  --height 40 \
  --chars " .':;!|/\\()[]{}<>*+#%@&$"
```

### 极简风格
```bash
python unicodeart.py -i minimal.jpg \
  --height 25 \
  --chars " █"
```

---

## 🎯 示例 5: 多行文本 Banner

**场景**: 制作多行标题

```
python unicodeart.py \
  -t "Hello\nWorld" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 15 \
  --line-spacing 1
```

**运行效果**:
终端会输出两行大型字符画，分别是 "Hello" 和 "World"，中间有指定的间距。具体样式取决于您使用的字体和终端显示设置。

**要点**:
- 使用 `\n` 分隔行
- `--line-spacing` 控制行间距

---

## 🎯 示例 6: 调整输出尺寸

**场景**: 控制字符画的大小

### 小尺寸（快速预览）
```bash
python unicodeart.py -i photo.jpg --height 15
```

### 中等尺寸（社交媒体）
```bash
python unicodeart.py -i photo.jpg --height 40
```

### 大尺寸（高质量）
```bash
python unicodeart.py -i photo.jpg --height 80
```

### 固定宽度
```bash
python unicodeart.py -i photo.jpg --height 30 --width 60
```

---

## 🎯 示例 7: 中文字符优化

**场景**: 获得更好的中文显示效果

```
python unicodeart.py \
  -t "你好世界" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 20 \
  --matrix 6
```

**关键参数**:
- `--font`: 使用支持中文的字体（宋体）
- `--matrix 6`: 平衡质量和速度
- **无需指定 ratio**: 默认 2.0 是标准值，适用于所有混合等宽字体环境

**重要说明**:
- `--ratio=2.0` + `--wide-char-ratio=2.0` 是**唯一正确配置**（在混合等宽字体显示环境中）
- 不要根据渲染字体调整 ratio，ratio 与显示环境的字体有关
- 如果观察到变形，检查您的终端/编辑器是否使用等宽字体

**对比测试**:
```bash
# ratio=2.0（可能变形）
python unicodeart.py -t "你" --font "SimSun.ttc" --ratio 2.0 --height 20 -o r2.txt

# ratio=1.2（推荐）
python unicodeart.py -t "你" --font "SimSun.ttc" --ratio 1.2 --height 20 -o r1.2.txt
```

---

## 🎯 示例 8: 反转颜色

**场景**: 深色背景终端或特殊效果

```bash
python unicodeart.py -i night_scene.jpg --height 30 --invert
```

**效果**: 
- 原本亮的区域变暗
- 原本暗的区域变亮

**适用场景**:
- 黑色背景终端
- 夜景照片
- 艺术创作

---

## 🎯 示例 9: 从文件读取文本

**场景**: 处理长文本或动态内容

### 步骤 1: 创建文本文件
```bash
# Windows
echo Hello UnicodeArt > message.txt

# Linux/macOS
echo "Hello UnicodeArt" > message.txt
```

### 步骤 2: 使用 @ 语法
```bash
python unicodeart.py \
  -t "@message.txt" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 15
```

**优势**:
- 支持任意长度文本
- 便于版本控制
- 可动态生成

---

## 🎯 示例 10: 调试模式

**场景**: 了解内部处理过程

```bash
python unicodeart.py \
  -i test.jpg \
  --height 10 \
  --debug sampling,matching
```

**输出示例**:
```
[sampling] Block size: 10x5 pixels
[sampling] Output dimensions: 30x60
[matching] Processing block (0,0)...
[matching] Best match: '@' (score: 123.45)
[matching] Processing block (0,1)...
[matching] Best match: '#' (score: 234.56)
...
```

**用途**:
- 学习算法原理
- 诊断问题
- 性能分析

---

## 💡 小贴士

### 提示 1: 选择合适的字符集

**低细节图形**（图标、Logo）:
```bash
--chars " ░█"  # 2-3 个字符
```

**中等细节**（人像、风景）:
```bash
--chars " .:-=+*#%@"  # 8-10 个字符（默认）
```

**高细节**（复杂场景）:
```bash
--chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"  # 60+ 字符
```

---

### 提示 2: 平衡速度和质量

**快速模式**（实时处理）:
```bash
--matrix 4 --interpolation nearest --height 20
```

**平衡模式**（推荐）:
```bash
--matrix 6 --interpolation bilinear --height 30
```

**高质量模式**（打印）:
```bash
--matrix 8 --interpolation lanczos --height 80
```

---

### 提示 3: 终端显示优化

**确保 UTF-8 编码**:
```bash
# Windows PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Linux/macOS
export LANG=en_US.UTF-8
```

**使用等宽字体终端**:
- Windows: Windows Terminal, ConEmu
- macOS: iTerm2, Terminal
- Linux: GNOME Terminal, Konsole

---

## 🎓 下一步

掌握了基础用法后，可以探索：

- 📚 [高级用法示例](advanced-options.md)
- 🎨 [自定义字符集](custom-chars.md)
- 🌏 [宽字符演示](wide-char-demo.md)

---

*最后更新: 2026-06-09*
