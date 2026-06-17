# 🚀 快速入门教程

本教程将在 **5 分钟**内带你完成 UnicodeArt 的基础使用。

---

## 📋 前置条件

确保你已完成 [安装](installation.md)，并准备好：
- ✅ Python 环境
- ✅ 字体文件（Windows 用户可使用 `C:\Windows\Fonts\SimSun.ttc`）
- ✅ 一张测试图片（可选）

---

## 🎨 示例 1: 文本转字符画（2 分钟）

### 基础用法

```bash
python unicodeart.py -t "Hello World" --font "C:\Windows\Fonts\SimSun.ttc" --height 10
```

**参数说明**:
- `-t`: 要转换的文本
- `--font`: 字体文件路径
- `--height`: 输出高度（行数）

**运行效果**:
在终端中会输出由字符组成的大型 "Hello World" 字样，具体样式取决于您使用的字体和终端显示设置。

### 多行文本

```bash
python unicodeart.py -t "第一行\n第二行\n第三行" --font "C:\Windows\Fonts\SimSun.ttc" --height 8
```

### 从文件读取文本

```bash
# 创建 test.txt 文件，写入内容
echo "Hello UnicodeArt" > test.txt

# 使用 @ 语法读取
python unicodeart.py -t "@test.txt" --font "C:\Windows\Fonts\SimSun.ttc" --height 10
```

---

## 🖼️ 示例 2: 图片转字符画（3 分钟）

### 基础用法

```bash
python unicodeart.py -i photo.jpg --height 30
```

**参数说明**:
- `-i` 或 `--image`: 输入图片路径
- `--height`: 输出高度（字符行数）

### 自定义字符集

```bash
# 使用自定义字符（从暗到亮）
python unicodeart.py -i photo.jpg --height 30 \
  --chars " .:-=+*#%@"
```

### 调整宽高比

```
# 默认 ratio=2.0，这是标准混合等宽字体的正确比例
# 在大多数现代终端和编辑器中（使用等宽字体显示），无需调整
python unicodeart.py -i photo.jpg --height 30
```

**重要说明**:
- `--ratio=2.0` 是**通用标准**，适用于所有混合等宽字体环境
- 只有在使用非等宽字体显示时，才可能需要微调
- 配合 `--wide-char-ratio=2.0` 确保宽字符正确识别

### 保存输出到文件

```bash
python unicodeart.py -i photo.jpg --height 30 -o output.txt
```

---

## ⚙️ 常用参数速查

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--text` | `-t` | 输入文本 | `-t "Hello"` |
| `--image` | `-i` | 输入图片 | `-i photo.jpg` |
| `--output` | `-o` | 输出文件 | `-o result.txt` |
| `--height` | | 输出高度 | `--height 30` |
| `--width` | | 输出宽度 | `--width 60` |
| `--font` | | 字体路径 | `--font "path/to/font.ttf"` |
| `--chars` | | 字符集 | `--chars " .:-=+*#%@"` |
| `--ratio` | `-r` | 高宽比 | `--ratio 2.0` |
| `--matrix` | `-m` | 采样矩阵大小 | `--matrix 6` |
| `--invert` | `-v` | 反转颜色 | `--invert` |
| `--font-style` | | 字体样式 | `--font-style bold` |
| `--font-reduce` | | 字体缩减量 | `--font-reduce 2` |
| `--interpolation` | | 插值算法 | `--interpolation bicubic` |
| `--wide-char-ratio` | | 宽字符比例 | `--wide-char-ratio 2.0` |
| `--height-mode` | | 高度模式 | `--height-mode line` |
| `--line-spacing` | | 行间距 | `--line-spacing 1` |

---

## 💡 实用技巧

### 技巧 1: 选择合适的输出高度

- **终端显示**: 20-40 行（避免超出屏幕）
- **社交媒体**: 50-100 行（更精细）
- **打印输出**: 100+ 行（最高质量）

### 技巧 2: 优化中文字符效果

```bash
# 宋体推荐配置
python unicodeart.py -t "你好世界" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 20 \
  --matrix 6 \
  --ratio 2.0
```

### 技巧 3: 处理高对比度图片

```bash
# 对于黑白分明的图片，使用较少字符
python unicodeart.py -i high_contrast.jpg \
  --height 30 \
  --chars " ░▒▓█"
```

### 技巧 4: 调试输出效果

```bash
# 使用 debug 模式查看详细过程
python unicodeart.py -i photo.jpg --height 20 -d sampling,matching
```

---

## 🎯 下一步学习

现在你已经掌握了基础用法，可以继续探索：

- 📚 [功能详细说明](features.md) - 深入了解每个参数
- 📖 [使用示例集](examples/) - 查看更多实战案例
- ❓ [常见问题解答](faq.md) - 解决遇到的问题

---

*最后更新: 2026-06-09*
