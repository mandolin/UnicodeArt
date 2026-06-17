# 📝 代码规范

本文档定义 UnicodeArt 项目的编码标准。

---

## 🐍 Python 代码风格

### 1. 格式化工具

**使用 Black 自动格式化**:
```bash
pip install black
black src/ tests/ tools/
```

**配置** (`pyproject.toml`):
```toml
[tool.black]
line-length = 88
target-version = ['py38']
```

---

### 2. 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量/函数 | snake_case | `get_sampling_array` |
| 类名 | PascalCase | `AlgorithmVisualizer` |
| 常量 | UPPER_SNAKE_CASE | `DEFAULT_MATRIX_SIZE` |
| 私有函数 | `_snake_case` | `_render_char_to_matrix` |
| 模块名 | snake_case | `unicodeart_util.py` |

---

### 3. 函数拆分原则

**最大行数**: 20-30 行

**单一职责**: 每个函数只做一件事

**示例**:
```python
# ✅ 良好：拆分为小函数
def get_char_data(...):
    chars = _load_characters(charset)
    matrices = [_render_char(c, ...) for c in chars]
    normalized = [_normalize(m) for m in matrices]
    return normalized

def _render_char(char, font, size):
    """渲染单个字符到矩阵"""
    # 10-15 行实现
    ...

def _normalize(matrix):
    """归一化矩阵到 [0, 1]"""
    # 5-10 行实现
    ...
```

---

### 4. 类型提示

**所有公共函数必须添加类型提示**:

```python
from typing import List, Tuple, Union
import numpy as np
from PIL import Image

def get_sampling_array(
    baseimg: Union[Image.Image, np.ndarray],
    height: int,
    width: int = None,
    matrix_size: int = 6
) -> np.ndarray:
    """生成采样数组
    
    Args:
        baseimg: 输入图像
        height: 输出高度
        width: 输出宽度
        matrix_size: 采样矩阵大小
    
    Returns:
        采样数组, shape (height, width, matrix_size, matrix_size)
    """
    ...
```

---

### 5. 文档字符串 (Docstring)

**格式**: Google Style

**必需内容**:
- 函数用途（一行简述）
- 详细说明（可选）
- Args: 参数说明
- Returns: 返回值说明
- Raises: 异常说明（如有）

**示例**:
```python
def get_final_output(
    sampling_array: np.ndarray,
    char_data: List[dict],
    wide_char_data: List[dict],
    output_path: str = None,
    wide_sum_ratio: float = 2.0
) -> str:
    """生成最终字符画
    
    通过 SAD 算法将采样块与字符矩阵匹配，组装成字符画字符串。
    
    Args:
        sampling_array: 采样数组, shape (R, C, M, M)
        char_data: 普通字符数据列表
        wide_char_data: 宽字符数据列表
        output_path: 输出文件路径（可选）
        wide_sum_ratio: 宽字符权重系数
    
    Returns:
        字符画字符串
    
    Raises:
        ValueError: 如果字符集为空
    
    Example:
        >>> output = get_final_output(sampling, char_data, wide_data)
        >>> print(output)
    """
    ...
```

---

## 🧪 测试规范

### 1. 测试文件命名

```
tests/test_<module_name>.py
```

**示例**:
- `test_character_matching.py`
- `test_image_sampling.py`

---

### 2. 测试函数命名

```python
def test_<function_name>_<scenario>():
```

**示例**:
```python
def test_get_sampling_array_with_valid_image():
    ...

def test_get_sampling_array_with_invalid_dimensions():
    ...
```

---

### 3. 断言风格

**使用 pytest 断言**:
```python
# ✅ 推荐
assert result.shape == (30, 40, 6, 6)
assert len(output) > 0

# ❌ 避免
self.assertEqual(result.shape, (30, 40, 6, 6))
```

**容差比较**（浮点数）:
```python
import pytest

# ✅ 允许误差
assert pytest.approx(score, abs=1e-6) == expected_score
```

---

### 4. Fixtures 使用

**共享资源通过 conftest.py**:
```python
# tests/fixtures/conftest.py
import pytest
import cv2

@pytest.fixture
def sample_image():
    """提供测试用图像"""
    return cv2.imread("tests/fixtures/test_images/small.png")

@pytest.fixture
def test_font():
    """提供测试用字体路径"""
    return "C:/Windows/Fonts/SimSun.ttc"
```

**在测试中使用**:
```python
def test_sampling(sample_image, test_font):
    sampling = get_sampling_array(sample_image, height=20)
    assert sampling is not None
```

---

## 📁 项目结构

```
UnicodeArt/
├── src/unicodeart/       # 源代码
│   ├── config/           # 配置模块
│   ├── console.py        # 控制流
│   └── unicodeart_util.py # 核心算法
├── tests/                # 测试代码
│   ├── fixtures/         # 测试资源
│   └── test_*.py         # 测试文件
├── doc/                  # 文档
│   ├── users/            # 用户文档
│   ├── devs/             # 开发者文档
│   ├── algorithms/       # 算法文档
│   └── porting/          # 移植文档
├── tools/                # 辅助工具
├── ai/tongyi/            # AI 协作区
└── dev/                  # 开发管理
```

---

## 🔧 Git 工作流

### 1. 分支策略

- `main`: 主分支（稳定版本）
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支

---

### 2. 提交信息规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具

**示例**:
```
feat(sampling): 添加 Lanczos 插值支持

- 新增 INTER_LANCZOS4 映射
- 更新文档说明性能对比

Closes #123
```

---

## 💡 最佳实践

### 1. 避免硬编码

```python
# ❌ 错误
matrix_size = 6
ratio = 2.0

# ✅ 正确
from config.constants import DEFAULT_MATRIX_SIZE, DEFAULT_VERTICAL_HORIZONTAL_RATIO
```

---

### 2. 错误处理

```python
# ✅ 防御性编程
if not Path(font_path).exists():
    raise FontLoadError(f"字体文件不存在: {font_path}")

image = cv2.imread(image_path)
if image is None:
    raise InvalidInputError(f"无法读取图像: {image_path}")
```

---

### 3. 日志记录

```python
import logging

logger = logging.getLogger(__name__)

def process_image(image_path):
    logger.info(f"Processing image: {image_path}")
    try:
        # ...
        logger.debug(f"Sampling array shape: {sampling.shape}")
    except Exception as e:
        logger.error(f"Failed to process image: {e}")
        raise
```

---

*最后更新: 2026-06-09*
