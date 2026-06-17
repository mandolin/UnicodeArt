# 🎨 自定义字符集示例

本文档展示如何根据场景选择合适的字符集。

---

## 📊 字符集选择原则

### 字符数量与细节

| 字符数 | 适用场景 | 效果 |
|--------|---------|------|
| 2-3 | 简单图标、Logo | 低细节，快速 |
| 5-8 | 人像、简单风景 | 中等细节 |
| 10-15 | 复杂照片 | 高细节 |
| 20+ | 艺术创作 | 极高细节 |

---

## 🎯 常用字符集推荐

### 1. 块状字符（终端友好）

```bash
--chars " ░▒▓█"
```

**特点**:
- Unicode 块状符号
- 视觉连续性好
- 适合深色背景终端

**示例**:
```bash
python unicodeart.py -i photo.jpg --height 30 --chars " ░▒▓█"
```

---

### 2. ASCII 经典字符集

```bash
--chars " .:-=+*#%@"
```

**特点**:
- 纯 ASCII，兼容性最好
- 默认字符集
- 适合所有终端

**示例**:
```bash
python unicodeart.py -i photo.jpg --height 30
# 等同于
python unicodeart.py -i photo.jpg --height 30 --chars " .:-=+*#%@"
```

---

### 3. 极简二值

```bash
--chars " █"
```

**特点**:
- 仅空格和实心块
- 类似黑白照片
- 适合高对比度图像

**示例**:
```bash
python unicodeart.py -i silhouette.jpg --height 30 --chars " █"
```

---

### 4. 丰富灰度级

```bash
--chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
```

**特点**:
- 70 个字符
- 极细腻过渡
- 适合高质量输出

**示例**:
```bash
python unicodeart.py -i landscape.jpg \
  --height 60 \
  --matrix 8 \
  --chars " .'`^\",:;Il!i><~_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
```

---

### 5. 数字风格

```bash
--chars " 0123456789"
```

**特点**:
- 科技感
- 适合数据可视化
- 独特美学

**示例**:
```bash
python unicodeart.py -i matrix_photo.jpg --height 30 --chars " 0123456789"
```

---

### 6. 括号艺术

```bash
--chars " ()[]{}<>"
```

**特点**:
- 几何感强
- 适合建筑、机械图
- 现代风格

**示例**:
```bash
python unicodeart.py -i architecture.jpg --height 30 --chars " ()[]{}<>"
```

---

## 🔧 自定义技巧

### 技巧 1: 从暗到亮排序

确保字符按亮度递增排列：

```bash
# ✅ 正确（从暗到亮）
--chars " .:-=+*#%@"

# ❌ 错误（乱序）
--chars "#@*.=-: "
```

**测试顺序**:
```bash
# 生成渐变测试图
python -c "
from PIL import Image, ImageDraw
img = Image.new('L', (256, 50))
draw = ImageDraw.Draw(img)
for x in range(256):
    draw.line([(x, 0), (x, 50)], fill=x)
img.save('gradient.png')
"

# 用不同字符集测试
python unicodeart.py -i gradient.png --height 10 --chars " YOUR_CHARS"
```

---

### 技巧 2: 去除重复亮度

避免使用亮度相近的字符：

```bash
# ❌ i 和 l 亮度接近
--chars " ...il..."

# ✅ 选择亮度差异大的
--chars " ...lI..."
```

---

### 技巧 3: 考虑字符宽度

等宽字符效果更好：

```bash
# ✅ 等宽
--chars " .:-=+*#%@"

# ⚠️ 不等宽（可能对齐问题）
--chars " .ijlw"
```

---

## 🎨 场景推荐

### 人像摄影
```bash
--chars " .':;!|/\\()[]{}<>*+#%@&$"
```

### 风景照
```bash
--chars " .:-=+*#%@"
```

### 建筑/城市
```bash
--chars " ()[]{}<>|/\\_"
```

### 夜景/高对比
```bash
--chars " ░▒▓█"
```

### 复古风格
```bash
--chars " .oO0#"
```

### 赛博朋克
```bash
--chars " 01XYZ#@%"
```

---

## 💡 实验建议

**快速测试不同字符集**:
```bash
#!/bin/bash
chars_sets=(
  " ░▒▓█"
  " .:-=+*#%@"
  " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
  " 0123456789"
)

for chars in "${chars_sets[@]}"; do
  python unicodeart.py -i test.jpg \
    --height 20 \
    --chars "$chars" \
    -o "output_$(echo $chars | md5sum | cut -d' ' -f1).txt"
done
```

---

*最后更新: 2026-06-09*
