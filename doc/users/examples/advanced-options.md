# ⚙️ 高级选项示例

本文档展示 UnicodeArt 的高级功能和参数组合。

---

## 🎯 示例 1: 高度模式对比

### Line 模式（默认）

```bash
python unicodeart.py \
  -t "A\nB\nC" \
  --font "SimSun.ttc" \
  --height 20 \
  --height-mode line \
  --line-spacing 1
```

**特点**:
- `--height` = 每行高度
- 总高度 = 20×3 + 1×2 = 62 像素
- 字体大小固定

---

### Total 模式

```bash
python unicodeart.py \
  -t "A\nB\nC" \
  --font "SimSun.ttc" \
  --height 60 \
  --height-mode total \
  --line-spacing 1
```

**特点**:
- `--height` = 总高度
- 自动计算每行高度 ≈ (60-2)/3 = 19 像素
- 适合固定显示区域

---

## 🎯 示例 2: 插值算法对比

```bash
# 最近邻（最快）
python unicodeart.py -i photo.jpg --height 30 --interpolation nearest -o out_nearest.txt

# 双线性（推荐）
python unicodeart.py -i photo.jpg --height 30 --interpolation bilinear -o out_bilinear.txt

# 双三次（较慢）
python unicodeart.py -i photo.jpg --height 30 --interpolation bicubic -o out_bicubic.txt

# Lanczos（最慢，最高质量）
python unicodeart.py -i photo.jpg --height 30 --interpolation lanczos -o out_lanczos.txt
```

**性能对比**:
| 算法 | 速度 | 质量 | 适用场景 |
|------|------|------|---------|
| nearest | ⚡⚡⚡⚡⚡ | ⭐⭐ | 实时预览 |
| bilinear | ⚡⚡⚡⚡ | ⭐⭐⭐ | 日常使用 |
| bicubic | ⚡⚡⚡ | ⭐⭐⭐⭐ | 高质量 |
| lanczos | ⚡⚡ | ⭐⭐⭐⭐⭐ | 打印输出 |

---

## 🎯 示例 3: 字体样式实验

```bash
# 正常
python unicodeart.py -t "Bold" --font "consola.ttf" --font-style normal --height 20

# 粗体
python unicodeart.py -t "Bold" --font "consola.ttf" --font-style bold --height 20

# 斜体
python unicodeart.py -t "Italic" --font "consola.ttf" --font-style italic --height 20

# 粗斜体
python unicodeart.py -t "Bold Italic" --font "consola.ttf" --font-style bold-italic --height 20
```

**注意**: 字体文件必须包含对应样式

---

## 🎯 示例 4: Font Reduce 调优

```bash
# 默认（无缩减）
python unicodeart.py -t "Test" --font "..." --font-reduce 0 --height 20

# 减少字体（增加留白）
python unicodeart.py -t "Test" --font "..." --font-reduce 2 --height 20

# 增大字体（减少留白）
python unicodeart.py -t "Test" --font "..." --font-reduce -1 --height 20
```

**视觉效果**:
- `reduce > 0`: 字符更紧凑，留白多
- `reduce < 0`: 字符更大，填充满

---

## 🎯 示例 5: Matrix 大小影响

```bash
# 快速低精度
python unicodeart.py -i photo.jpg --matrix 4 --height 30 -o m4.txt

# 平衡（推荐）
python unicodeart.py -i photo.jpg --matrix 6 --height 30 -o m6.txt

# 高精度
python unicodeart.py -i photo.jpg --matrix 8 --height 30 -o m8.txt

# 超高精度
python unicodeart.py -i photo.jpg --matrix 10 --height 30 -o m10.txt
```

**性能影响**:
- `matrix=4`: 基准速度
- `matrix=6`: ~2.25× 慢
- `matrix=8`: ~4× 慢
- `matrix=10`: ~6.25× 慢

---

## 🎯 示例 6: Ratio 参数说明

### 标准配置（推荐）

```bash
# 在混合等宽字体显示环境中，ratio=2.0 是唯一正确值
python unicodeart.py -t "中文测试" \
  --font "SimSun.ttc" \
  --ratio 2.0 \
  --height 20
```

**重要概念**:
- `--ratio` 与**渲染字体**（--font）无关
- `--ratio=2.0` 假设您的**显示环境**使用混合等宽字体
- 在 VSCode、Windows Terminal、浏览器中，默认就是混合等宽字体

### 何时需要调整 ratio？

**只有在以下情况才需要调整**:
1. 您的终端/编辑器使用的**显示字体**不是混合等宽字体
2. 观察到字符画整体变形

**解决方式**: 
- ✅ **优先**: 调整显示环境的字体设置为等宽字体
- ⚠️ **备选**: 微调 ratio 参数（不推荐）

### 测试脚本

```bash
# 测试标准配置（应该正常）
python unicodeart.py -t "A" --font "SimSun.ttc" --ratio 2.0 --height 20 -o ratio_2.0.txt

# 如果仍然变形，检查显示环境字体设置
# 而不是尝试不同 ratio 值
```

---

## 🎯 示例 7: 宽字符比例调优

```bash
# 积极使用中文
python unicodeart.py -i mixed_text.jpg \
  --height 30 \
  --wide-char-ratio 1.5

# 平衡（默认）
python unicodeart.py -i mixed_text.jpg \
  --height 30 \
  --wide-char-ratio 2.0

# 保守使用中文
python unicodeart.py -i mixed_text.jpg \
  --height 30 \
  --wide-char-ratio 3.0
```

**选择建议**:
- 中文为主: `1.5`
- 中英混合: `2.0`
- 英文为主: `2.5-3.0`

---

## 🎯 示例 8: 调试模式详解

```bash
# 查看采样过程
python unicodeart.py -i test.jpg --height 10 --debug sampling

# 查看匹配过程
python unicodeart.py -i test.jpg --height 10 --debug matching

# 全部信息
python unicodeart.py -i test.jpg --height 10 --debug all
```

**输出示例**:
```
[sampling] Source image: 800x600
[sampling] Output size: 30x40
[sampling] Block size: 20x20 pixels
[matching] Block (0,0): best='@' score=123.45
[matching] Block (0,1): best='#' score=234.56
...
```

---

## 🎯 示例 9: 批量处理脚本

### Bash 脚本（Linux/macOS）

```bash
#!/bin/bash
# batch_convert.sh

INPUT_DIR="photos"
OUTPUT_DIR="output"
HEIGHT=30

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.jpg; do
  basename=$(basename "$img" .jpg)
  echo "Processing: $basename"
  python unicodeart.py -i "$img" \
    --height $HEIGHT \
    -o "$OUTPUT_DIR/${basename}.txt"
done

echo "Done! Processed $(ls "$OUTPUT_DIR"/*.txt | wc -l) files."
```

**使用**:
```bash
chmod +x batch_convert.sh
./batch_convert.sh
```

---

### PowerShell 脚本（Windows）

```
# batch_convert.ps1

$InputDir = "photos"
$OutputDir = "output"
$Height = 30

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

Get-ChildItem "$InputDir\*.jpg" | ForEach-Object {
    $basename = $_.BaseName
    Write-Host "Processing: $basename"
    
    python unicodeart.py -i $_.FullName `
      --height $Height `
      -o "$OutputDir\$basename.txt"
}

Write-Host "Done! Processed $((Get-ChildItem "$OutputDir\*.txt").Count) files."
```

**使用**:
```
.\batch_convert.ps1
```

---

## 🎯 示例 10: Python API 调用

```python
import sys
sys.path.insert(0, 'src')

from unicodeart.unicodeart_util import (
    get_sampling_array,
    get_char_data,
    get_final_output
)
import cv2

def convert_image(image_path, height=30, matrix_size=6):
    """将图像转换为字符画"""
    # 加载图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # 生成采样数组
    sampling = get_sampling_array(
        image, 
        height=height, 
        width=None, 
        matrix_size=matrix_size
    )
    
    # 预计算字符矩阵（可缓存）
    char_data, wide_data = get_char_data(
        None,  # 使用默认字符集
        r"C:\Windows\Fonts\SimSun.ttc",
        matrix_size=matrix_size,
        vertical_horizontal_ratio=2.0
    )
    
    # 生成输出
    output = get_final_output(
        sampling,
        char_data,
        wide_data,
        output_path=None,
        wide_sum_ratio=2.0
    )
    
    return output

# 使用示例
if __name__ == "__main__":
    result = convert_image("photo.jpg", height=30)
    print(result)
    
    # 保存到文件
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(result)
```

---

## 💡 高级技巧

### 技巧 1: 缓存字符矩阵

```python
# 多次转换时复用 char_data
char_data, wide_data = get_char_data(...)

for image_path in image_list:
    sampling = get_sampling_array(load_image(image_path), ...)
    output = get_final_output(sampling, char_data, wide_data, ...)
```

**性能提升**: 避免重复渲染字体（节省 30-50% 时间）

---

### 技巧 2: 动态调整高度

```python
def auto_height(image_path, target_width=80):
    """根据图片宽高比自动计算合适的高度"""
    import cv2
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    aspect_ratio = h / w
    return int(target_width * aspect_ratio)

height = auto_height("photo.jpg")
python unicodeart.py -i photo.jpg --height $height
```

---

### 技巧 3: 质量评估

```python
def evaluate_quality(output_text):
    """简单评估字符画质量"""
    lines = output_text.strip().split('\n')
    
    # 检查一致性
    widths = [len(line) for line in lines]
    variance = sum((w - sum(widths)/len(widths))**2 for w in widths) / len(widths)
    
    # 方差越小，质量越好
    return variance

quality = evaluate_quality(output)
print(f"Quality score: {quality:.2f} (lower is better)")
```

---

*最后更新: 2026-06-09*
