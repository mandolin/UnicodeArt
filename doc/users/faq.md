# ❓ 常见问题解答 (FAQ)

本文档汇总了使用 UnicodeArt 时最常见的问题和解决方案。

---

## 📦 安装相关问题

### Q1: 安装后运行提示 `ModuleNotFoundError`

**问题**: 
```
ModuleNotFoundError: No module named 'cv2'
ModuleNotFoundError: No module named 'PIL'
```

**原因**: 依赖库未正确安装

**解决**:
```bash
# 重新安装所有依赖
pip install -r requirements.txt

# 或单独安装缺失的库
pip install opencv-python
pip install Pillow
pip install numpy
```

---

### Q2: 字体文件找不到

**问题**: 
```
OSError: cannot open resource
```

**原因**: 字体路径错误或文件不存在

**解决**:
1. **确认文件存在**:
   ```bash
   # Windows
   dir "C:\Windows\Fonts\SimSun.ttc"
   
   # macOS
   ls /Library/Fonts/PingFang.ttc
   
   # Linux
   ls /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
   ```

2. **使用绝对路径**:
   ```bash
   # ✅ 正确
   --font "C:\Windows\Fonts\SimSun.ttc"
   
   # ❌ 错误（相对路径可能找不到）
   --font "SimSun.ttc"
   ```

3. **检查路径分隔符**:
   ```bash
   # Windows 两种写法都可以
   --font "C:\Windows\Fonts\SimSun.ttc"
   --font "C:/Windows/Fonts/SimSun.ttc"
   ```

---

### Q3: 中文字符显示为方块

**问题**: 终端输出中中文显示为 `□□□` 或乱码

**原因**: 
1. 字体不支持中文
2. 终端编码不是 UTF-8

**解决**:

**Windows PowerShell**:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python unicodeart.py -t "你好" --font "C:\Windows\Fonts\SimSun.ttc" --height 15
```

**Linux/macOS**:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
python unicodeart.py -t "你好" --font "/path/to/chinese-font.ttf" --height 15
```

**使用支持中文的字体**:
- Windows: 宋体 (`SimSun.ttc`)、微软雅黑 (`MSYH.TTC`)
- macOS: 苹方 (`PingFang.ttc`)
- Linux: 文泉驿 (`wqy-zenhei.ttc`)

---

## 🎨 输出效果问题

### Q4: 字符画变形或拉伸

**问题**: 生成的字符画看起来被压扁或拉长

**原因**: 
1. `--ratio` 参数设置不当
2. **更常见的原因**: 显示环境（终端/编辑器）使用的字体不是混合等宽字体

**重要概念区分**:
- **渲染字体** (`--font`): 用来生成字符画的字体（如 SimSun.ttc）
- **显示字体**: 您的终端/编辑器用来显示输出结果的字体

**正确理解**:
- `--ratio=2.0` 是**标准值**，假设您的**显示环境**使用混合等宽字体
- 在 VSCode、大多数现代终端中，默认就是混合等宽字体，**无需调整 ratio**
- 只有当您的显示环境使用非等宽字体时，才需要微调 ratio

**解决步骤**:

**步骤 1: 确认显示环境**
```bash
# 检查您的终端/编辑器是否使用等宽字体
# VSCode: 查看设置中的 "Font Family"
# Windows Terminal: 查看配置文件中的 fontFace
```

**步骤 2: 使用标准配置测试**
```bash
# 推荐配置（适用于绝大多数环境）
python unicodeart.py -t "测试" --font "SimSun.ttc" --ratio 2.0 --height 20
```

**步骤 3: 如果仍然变形，检查显示字体**
- 确保终端/编辑器使用等宽字体（如 Consolas, Courier New, 等）
- 不要调整 ratio，而是调整显示环境的字体设置

**快速诊断**:
```bash
# 生成不同 ratio 的对比，观察哪个最正常
for ratio in 1.5 2.0 2.5; do
  python unicodeart.py -t "A" --font "SimSun.ttc" --ratio $ratio --height 20 -o "ratio_${ratio}.txt"
done
# 通常 ratio=2.0 是最正常的
```

---

### Q5: 输出太模糊或缺乏细节

**问题**: 字符画看起来很粗糙，细节不足

**原因**: 
1. `--matrix` 太小
2. `--chars` 字符集太少
3. 输出高度太低

**解决**:

**增加采样精度**:
```bash
# 从默认 6 增加到 8 或 10
python unicodeart.py -i photo.jpg --matrix 8 --height 50
```

**使用更多字符**:
```bash
# 丰富字符集
python unicodeart.py -i photo.jpg \
  --chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" \
  --height 50
```

**增加输出尺寸**:
```bash
# 从 30 行增加到 80 行
python unicodeart.py -i photo.jpg --height 80
```

---

### Q6: 输出太慢

**问题**: 处理大图片或高 `--height` 时非常慢

**原因**: 
1. 输出尺寸太大
2. `--matrix` 太大
3. 插值算法太慢

**解决**:

**降低输出尺寸**:
```bash
# 从 100 降到 40
python unicodeart.py -i photo.jpg --height 40
```

**减小 matrix**:
```bash
# 从 8 降到 4（速度提升约 4 倍）
python unicodeart.py -i photo.jpg --matrix 4 --height 40
```

**使用快速插值**:
```bash
# nearest 最快
python unicodeart.py -i photo.jpg --interpolation nearest --height 40
```

**性能对比**:
| 配置 | 相对速度 |
|------|---------|
| `matrix=4, nearest` | ⚡⚡⚡⚡⚡ 最快 |
| `matrix=6, bilinear` | ⚡⚡⚡⚡ 推荐 |
| `matrix=8, bicubic` | ⚡⚡⚡ 较慢 |
| `matrix=10, lanczos` | ⚡⚡ 最慢 |

---

### Q7: 宽字符（中文）识别不准确

**问题**: 应该用中文字符的地方用了英文字符，或反之

**原因**: `--wide-char-ratio` 设置不当

**解决**:

**优先使用宽字符**:
```bash
# 降低阈值（默认 2.0）
python unicodeart.py -i photo.jpg --wide-char-ratio 1.5
```

**谨慎使用宽字符**:
```bash
# 提高阈值
python unicodeart.py -i photo.jpg --wide-char-ratio 3.0
```

**自定义宽字符集**:
```bash
# 只使用特定中文字符
python unicodeart.py -i photo.jpg --wide-chars "一二三四五六七八九十"
```

---

## 📝 文本模式问题

### Q8: 多行文本行间距太大或太小

**问题**: 多行文本之间的间距不符合预期

**原因**: `--line-spacing` 设置问题

**解决**:

**调整行间距**:
```bash
# 无间距（紧凑）
python unicodeart.py -t "A\nB\nC" --line-spacing 0 --height 15

# 1 行间距（适中）
python unicodeart.py -t "A\nB\nC" --line-spacing 1 --height 15

# 2 行间距（宽松）
python unicodeart.py -t "A\nB\nC" --line-spacing 2 --height 15
```

**注意**: `--height-mode` 会影响总高度计算
- `line` 模式: 总高度 = 每行高度 × 行数 + 间距
- `total` 模式: 总高度固定，自动分配

---

### Q9: 文本模式下字体大小不一致

**问题**: 有行间距时字体变小了

**原因**: 在 `line` 模式下错误地从字体高度中扣除了行间距

**解决**: 确保使用正确的 `--height-mode`

```bash
# line 模式（默认）: 字体大小不受行间距影响
python unicodeart.py -t "A\nB" --height 20 --line-spacing 1 --height-mode line

# total 模式: 字体会根据总高度自动调整
python unicodeart.py -t "A\nB" --height 40 --line-spacing 1 --height-mode total
```

---

## 🖼️ 图片模式问题

### Q10: 图片加载失败

**问题**: 
```
err:无法读取图像
```

**原因**: 
1. 文件路径错误
2. 文件格式不支持
3. 文件损坏

**解决**:

**检查文件是否存在**:
```bash
# Windows
dir photo.jpg

# Linux/macOS
ls -l photo.jpg
```

**验证文件格式**:
```bash
# 使用 Python 检查
python -c "import cv2; img = cv2.imread('photo.jpg'); print('OK' if img is not None else 'FAIL')"
```

**转换格式**:
```bash
# 如果格式不支持，用 PIL 转换
python -c "from PIL import Image; Image.open('input.bmp').save('output.png')"
```

---

### Q11: 输出宽高比不正确

**问题**: 生成的字符画被压扁或拉长

**原因**: 未指定 `--width` 时自动计算的宽高比不符合预期

**解决**:

**手动指定宽度**:
```bash
# 固定宽度 80 字符
python unicodeart.py -i photo.jpg --height 30 --width 80
```

**保持原始宽高比**:
```bash
# 不指定 --width，自动计算
python unicodeart.py -i photo.jpg --height 30
```

**调整 ratio**:
```bash
# 如果字符本身变形，调整 ratio
python unicodeart.py -i photo.jpg --height 30 --ratio 1.5
```

---

## 🔧 高级问题

### Q12: 如何在脚本中调用 UnicodeArt？

**问题**: 想在 Python 代码中使用，而非命令行

**解决**:

**方法 1: 使用 subprocess**:
```python
import subprocess

result = subprocess.run([
    'python', 'unicodeart.py',
    '-i', 'photo.jpg',
    '--height', '30',
    '-o', 'output.txt'
], capture_output=True, text=True)

print(result.stdout)
```

**方法 2: 直接导入模块**（推荐）:
```python
import sys
sys.path.insert(0, 'src')

from unicodeart.unicodeart_util import (
    get_baseimg,
    get_sampling_array,
    get_char_data,
    get_final_output
)
import cv2

# 加载图像
image = cv2.imread('photo.jpg', cv2.IMREAD_GRAYSCALE)

# 生成采样数组
sampling = get_sampling_array(image, height=30, width=None, matrix_size=6)

# 预计算字符矩阵
char_data, wide_data = get_char_data(None, font_path, matrix_size=6)

# 生成输出
output = get_final_output(sampling, char_data, wide_data)

print(output)
```

---

### Q13: 如何自定义字符匹配算法？

**问题**: 想使用 SAD 之外的匹配方法

**解决**: 目前仅支持 SAD（Sum of Absolute Differences）

**未来计划**: 
- SSD（Sum of Squared Differences）
- NCC（Normalized Cross-Correlation）
- 机器学习方法

**临时方案**: 修改 `src/unicodeart/unicodeart_util.py` 中的匹配逻辑

---

### Q14: 内存占用太高怎么办？

**问题**: 处理大图时内存溢出

**原因**: 
1. 采样数组太大
2. 字符矩阵缓存太多

**解决**:

**降低输出尺寸**:
```bash
python unicodeart.py -i large_photo.jpg --height 20  # 而非 100
```

**减小 matrix**:
```bash
python unicodeart.py -i large_photo.jpg --matrix 4  # 而非 8
```

**分批处理**（超大图片）:
```python
# 将图片分割成小块分别处理
# 需要自行实现拼接逻辑
```

---

### Q15: 如何获得彩色字符画？

**问题**: 当前只支持灰度/黑白输出

**回答**: 目前版本**不支持彩色**

**原因**: 
- 核心算法基于灰度矩阵匹配
- 彩色需要 RGB 三通道处理，复杂度增加 3 倍

**替代方案**:
1. 使用 HTML/CSS 着色（后处理）
2. ANSI 转义码（终端彩色）
3. 等待未来版本支持

---

## 📊 性能优化

### Q16: 如何加速批量处理？

**问题**: 需要处理大量图片

**解决**:

**方法 1: 并行处理**:
```bash
# 使用 GNU Parallel（Linux/macOS）
ls *.jpg | parallel python unicodeart.py -i {} --height 30 -o {.}.txt

# Windows PowerShell
Get-ChildItem *.jpg | ForEach-Object {
    Start-Job -ScriptBlock {
        python unicodeart.py -i $args[0] --height 30 -o "$($args[0].BaseName).txt"
    } -ArgumentList $_
}
```

**方法 2: 降低质量换取速度**:
```bash
python unicodeart.py -i photo.jpg --matrix 4 --interpolation nearest --height 20
```

**方法 3: 缓存字符矩阵**:
```python
# 多次运行时复用 char_data
char_data, wide_data = get_char_data(...)  # 只计算一次
for image in images:
    sampling = get_sampling_array(image, ...)
    output = get_final_output(sampling, char_data, wide_data)
```

---

## 🎯 最佳实践

### ✅ 推荐配置

**终端快速预览**:
```bash
python unicodeart.py -i photo.jpg \
  --height 20 \
  --matrix 4 \
  --interpolation nearest \
  --chars " ░▒▓█"
```

**社交媒体分享**:
```bash
python unicodeart.py -i photo.jpg \
  --height 50 \
  --matrix 6 \
  --interpolation bilinear \
  --chars " .:-=+*#%@" \
  -o output.txt
```

**高质量打印**:
```bash
python unicodeart.py -i photo.jpg \
  --height 100 \
  --matrix 8 \
  --interpolation lanczos \
  --chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" \
  -o output.txt
```

**中文文本 Banner**:
```bash
python unicodeart.py -t "你好世界" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 20 \
  --matrix 6 \
  --ratio 1.2
```

---

## 📞 获取帮助

如果以上未能解决你的问题：

1. **查看文档**:
   - 📖 [功能详细说明](features.md)
   - 🚀 [快速入门](quick-start.md)

2. **检查 Issue**:
   - GitHub Issues: https://github.com/your-username/UnicodeArt/issues

3. **提交新问题**:
   - 提供完整命令
   - 附上错误信息
   - 说明预期行为和实际行为

---

*最后更新: 2026-06-09*
