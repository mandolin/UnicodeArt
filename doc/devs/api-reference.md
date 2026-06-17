# 📖 API 参考文档

本文档列出 UnicodeArt 的所有公共 API。

---

## 🎯 核心函数

### get_baseimg()

**用途**: 将文本渲染为图像

**签名**:
```python
def get_baseimg(
    text_string: str,
    art_font: str,
    height: int,
    matrix_size: int,
    text_align: str = 'left',
    line_spacing: int = 0,
    height_mode: str = 'line',
    fontreduce: int = None
) -> Image.Image
```

**参数**:
- `text_string`: 文本内容（支持 `\n` 多行和 `@file.txt` 语法）
- `art_font`: 字体文件路径（.ttf/.ttc）
- `height`: 高度（含义取决于 `height_mode`）
- `matrix_size`: 采样矩阵大小
- `text_align`: 对齐方式 (`'left'`, `'center'`, `'right'`)
- `line_spacing`: 行间距（字符画行数）
- `height_mode`: 高度模式 (`'line'` 或 `'total'`)
- `fontreduce`: 字体缩减量（默认: `DEFAULT_FONT_REDUCE`）

**返回**: PIL Image 对象（灰度）

**示例**:
```python
from unicodeart.unicodeart_util import get_baseimg

img = get_baseimg(
    "Hello\nWorld",
    "C:/Windows/Fonts/SimSun.ttc",
    height=20,
    matrix_size=6,
    height_mode='line'
)
```

---

### get_sampling_array()

**用途**: 将图像转换为采样数组

**签名**:
```python
def get_sampling_array(
    baseimg: Union[Image.Image, np.ndarray],
    height: int,
    width: int = None,
    matrix_size: int = 6,
    interpolation: str = 'bilinear'
) -> np.ndarray
```

**参数**:
- `baseimg`: 输入图像（PIL Image 或 numpy array）
- `height`: 输出高度（行数）
- `width`: 输出宽度（列数，可选）
- `matrix_size`: 采样矩阵大小
- `interpolation`: 插值算法 (`'nearest'`, `'bilinear'`, `'bicubic'`, `'lanczos'`)

**返回**: numpy array, shape `(height, width, matrix_size, matrix_size)`，值域 [0, 1]

**示例**:
```python
import cv2
from unicodeart.unicodeart_util import get_sampling_array

image = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)
sampling = get_sampling_array(image, height=30, matrix_size=6)
print(sampling.shape)  # (30, 40, 6, 6)
```

---

### get_char_data()

**用途**: 预计算字符矩阵

**签名**:
```python
def get_char_data(
    charset: List[str] = None,
    font_path: str = None,
    matrix_size: int = 6,
    vertical_horizontal_ratio: float = 2.0,
    wide_charset: List[str] = None,
    interpolation: str = 'bilinear'
) -> Tuple[List[dict], List[dict]]
```

**参数**:
- `charset`: 普通字符集（默认: `" .:-=+*#%@"`）
- `font_path`: 字体文件路径
- `matrix_size`: 矩阵大小
- `vertical_horizontal_ratio`: 高宽比
- `wide_charset`: 宽字符集（默认: 自动识别）
- `interpolation`: 插值算法

**返回**: `(char_data, wide_char_data)`，每个元素为 list of dict:
```python
{
    'character': 'A',
    'matrix': np.ndarray,  # shape: (M, M) or (2M, M) for wide
    'is_wide': False
}
```

**示例**:
```python
from unicodeart.unicodeart_util import get_char_data

char_data, wide_data = get_char_data(
    font_path="C:/Windows/Fonts/SimSun.ttc",
    matrix_size=6,
    vertical_horizontal_ratio=2.0
)

print(len(char_data))     # 10
print(len(wide_data))     # 数千个中文字符
```

**性能提示**: 此函数较慢，建议缓存结果

---

### get_final_output()

**用途**: 生成最终字符画

**签名**:
```python
def get_final_output(
    sampling_array: np.ndarray,
    char_data: List[dict],
    wide_char_data: List[dict],
    output_path: str = None,
    wide_sum_ratio: float = 2.0
) -> str
```

**参数**:
- `sampling_array`: 采样数组
- `char_data`: 普通字符数据
- `wide_char_data`: 宽字符数据
- `output_path`: 输出文件路径（可选）
- `wide_sum_ratio`: 宽字符权重

**返回**: 字符画字符串

**示例**:
```python
from unicodeart.unicodeart_util import get_final_output

output = get_final_output(
    sampling_array,
    char_data,
    wide_data,
    output_path="result.txt",
    wide_sum_ratio=2.0
)

print(output)
```

---

## 🔧 辅助函数

### preprocess_text_input()

**用途**: 预处理文本输入

**签名**:
```python
def preprocess_text_input(text_string: str) -> List[str]
```

**参数**:
- `text_string`: 原始文本（支持 `@file.txt` 语法）

**返回**: 文本行列表

**示例**:
```python
lines = preprocess_text_input("Line1\nLine2")
# ['Line1', 'Line2']

lines = preprocess_text_input("@test.txt")
# ['content from file']
```

---

### _decide_character_type()

**用途**: 判断字符类型（普通/宽字符）

**签名**:
```python
def _decide_character_type(char: str) -> str
```

**返回**: `'normal'` 或 `'wide'`

**注意**: 私有函数（`_` 前缀），不建议直接调用

---

## 📦 常量配置

所有常量定义在 `src/unicodeart/config/constants.py`

### 主要常量

```python
DEFAULT_MATRIX_SIZE = 6
DEFAULT_VERTICAL_HORIZONTAL_RATIO = 2.0
DEFAULT_FONT_REDUCE = 0
DEFAULT_WIDE_CHAR_RATIO = 2.0
DEFAULT_CHARS = " .:-=+*#%@"
MAX_SUM_DATA = 1000000
PIXEL_MAX_VALUE = 255.0
```

### 插值算法映射

```python
INTERPOLATION_MAP = {
    'nearest': cv2.INTER_NEAREST,
    'bilinear': cv2.INTER_LINEAR,
    'bicubic': cv2.INTER_CUBIC,
    'lanczos': cv2.INTER_LANCZOS4
}
```

---

## 🎨 使用示例

### 完整流程示例

```python
import sys
sys.path.insert(0, 'src')

import cv2
from unicodeart.unicodeart_util import (
    get_sampling_array,
    get_char_data,
    get_final_output
)

# 1. 加载图像
image = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)

# 2. 生成采样数组
sampling = get_sampling_array(
    image, 
    height=30, 
    matrix_size=6
)

# 3. 预计算字符矩阵（可缓存）
char_data, wide_data = get_char_data(
    font_path="C:/Windows/Fonts/SimSun.ttc",
    matrix_size=6,
    vertical_horizontal_ratio=2.0
)

# 4. 生成输出
output = get_final_output(
    sampling,
    char_data,
    wide_data,
    output_path="result.txt"
)

print(output)
```

---

### 批量处理示例

```python
# 缓存字符矩阵
char_data, wide_data = get_char_data(...)

for image_path in ["photo1.jpg", "photo2.jpg", "photo3.jpg"]:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    sampling = get_sampling_array(image, height=30)
    output = get_final_output(sampling, char_data, wide_data)
    
    with open(f"{image_path}.txt", "w") as f:
        f.write(output)
```

**性能提升**: 避免重复渲染字体（节省 30-50% 时间）

---

## ⚠️ 注意事项

### 1. 线程安全

当前实现**不是线程安全的**。多线程使用时需加锁：

```python
import threading
lock = threading.Lock()

with lock:
    output = get_final_output(...)
```

---

### 2. 内存管理

大图像可能占用大量内存：

```python
# 监控内存
import tracemalloc
tracemalloc.start()

# ... 执行转换 ...

current, peak = tracemalloc.get_traced_memory()
print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()
```

---

### 3. 异常处理

所有函数可能抛出的异常：

| 异常 | 原因 |
|------|------|
| `FileNotFoundError` | 文件不存在 |
| `ValueError` | 参数无效 |
| `OSError` | 字体加载失败 |
| `MemoryError` | 内存不足 |

**建议**:
```python
try:
    output = get_final_output(...)
except FileNotFoundError as e:
    print(f"文件未找到: {e}")
except ValueError as e:
    print(f"参数错误: {e}")
```

---

## 📚 相关文档

- 🏗️ [架构设计](architecture.md)
- 📝 [代码规范](coding-standards.md)
- 🚀 [扩展开发](extending.md)

---

*最后更新: 2026-06-09*
