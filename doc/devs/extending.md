# 🚀 扩展开发指南

本文档说明如何为 UnicodeArt 添加新功能。

---

## 🎯 扩展点概览

### 1. 添加新的匹配算法

### 2. 支持彩色输出

### 3. 添加新的输出格式

### 4. 自定义字符集加载

### 5. 插件化架构（未来）

---

## 🔧 示例 1: 添加 SSD 匹配算法

### 步骤 1: 实现算法函数

在 `src/unicodeart/unicodeart_util.py` 中添加：

```python
def _ssd_matching(block: np.ndarray, char_matrix: np.ndarray) -> float:
    """SSD (Sum of Squared Differences) 匹配算法
    
    Args:
        block: 采样块矩阵
        char_matrix: 字符矩阵
    
    Returns:
        SSD 得分（越小越相似）
    """
    diff = block - char_matrix
    return np.sum(diff ** 2)
```

---

### 步骤 2: 修改匹配逻辑

在 `get_final_output()` 中添加算法选择：

```python
def get_final_output(
    ...,
    matching_algorithm: str = 'sad'  # 新增参数
) -> str:
    """..."""
    
    # 选择匹配算法
    if matching_algorithm == 'sad':
        score_func = lambda b, c: np.sum(np.abs(b - c))
    elif matching_algorithm == 'ssd':
        score_func = _ssd_matching
    else:
        raise ValueError(f"Unknown algorithm: {matching_algorithm}")
    
    # 使用选定的算法
    for block in sampling_array:
        best_score = float('inf')
        best_char = None
        
        for char_info in char_data + wide_char_data:
            score = score_func(block, char_info['matrix'])
            if score < best_score:
                best_score = score
                best_char = char_info['character']
        
        output += best_char
```

---

### 步骤 3: 添加命令行参数

在 `src/unicodeart/console.py` 的 `parse_arguments()` 中：

```python
p.add_argument('--matching-algo', 
               choices=['sad', 'ssd'],
               default='sad',
               help='字符匹配算法 (默认: sad)')
```

---

### 步骤 4: 传递参数

在 `main()` 中调用时传递：

```python
output = get_final_output(
    sampling_array,
    char_data,
    wide_char_data,
    matching_algorithm=args.matching_algo
)
```

---

### 步骤 5: 添加测试

创建 `tests/test_ssd_matching.py`:

```python
import pytest
import numpy as np
from unicodeart.unicodeart_util import _ssd_matching

def test_ssd_matching_identical():
    """相同矩阵应得分为 0"""
    matrix = np.random.rand(6, 6)
    score = _ssd_matching(matrix, matrix)
    assert score == 0.0

def test_ssd_matching_different():
    """不同矩阵应得分 > 0"""
    m1 = np.zeros((6, 6))
    m2 = np.ones((6, 6))
    score = _ssd_matching(m1, m2)
    assert score > 0.0
```

---

### 步骤 6: 更新文档

在 [API 参考](api-reference.md) 中添加新参数说明。

---

## 🎨 示例 2: 支持彩色输出

### 挑战

- 采样数组需扩展为 `(R, C, M, M, 3)`
- 匹配算法需考虑 RGB 三通道

---

### 步骤 1: 扩展数据结构

```python
def get_sampling_array_rgb(
    baseimg: np.ndarray,  # 现在是 3 通道
    height: int,
    width: int = None,
    matrix_size: int = 6
) -> np.ndarray:
    """生成 RGB 采样数组
    
    Returns:
        shape: (height, width, matrix_size, matrix_size, 3)
    """
    # 处理每个通道
    r_channel = process_channel(baseimg[:, :, 0], ...)
    g_channel = process_channel(baseimg[:, :, 1], ...)
    b_channel = process_channel(baseimg[:, :, 2], ...)
    
    # 合并
    sampling_rgb = np.stack([r_channel, g_channel, b_channel], axis=-1)
    return sampling_rgb
```

---

### 步骤 2: 颜色距离计算

```python
def _color_distance(rgb1: np.ndarray, rgb2: np.ndarray) -> float:
    """计算两个 RGB 值的欧氏距离
    
    Args:
        rgb1: shape (M, M, 3)
        rgb2: shape (M, M, 3)
    
    Returns:
        距离值
    """
    diff = rgb1 - rgb2
    return np.sqrt(np.sum(diff ** 2))
```

---

### 步骤 3: 渲染彩色字符

```python
def _render_char_to_matrix_rgb(
    char: str,
    font,
    size: int,
    matrix_size: int
) -> np.ndarray:
    """渲染字符为 RGB 矩阵
    
    Returns:
        shape: (2*matrix_size, matrix_size, 3) for wide chars
    """
    # 类似灰度版本，但保留 RGB 信息
    ...
```

---

### 步骤 4: ANSI 输出

```python
def output_ansi(sampling_rgb, char_data_rgb):
    """生成 ANSI 彩色输出"""
    output = []
    
    for row in range(sampling_rgb.shape[0]):
        line = []
        for col in range(sampling_rgb.shape[1]):
            block = sampling_rgb[row, col]
            
            # 找到最佳匹配（考虑颜色）
            best_char, avg_color = match_with_color(block, char_data_rgb)
            
            # ANSI 转义码
            r, g, b = avg_color.astype(int)
            ansi_code = f"\033[38;2;{r};{g};{b}m"
            line.append(f"{ansi_code}{best_char}\033[0m")
        
        output.append(''.join(line))
    
    return '\n'.join(output)
```

---

### 步骤 5: HTML 输出

```python
def output_html(sampling_rgb, char_data_rgb):
    """生成 HTML 彩色输出"""
    html = ['<pre style="line-height:1;">']
    
    for row in range(sampling_rgb.shape[0]):
        for col in range(sampling_rgb.shape[1]):
            block = sampling_rgb[row, col]
            best_char, avg_color = match_with_color(block, char_data_rgb)
            
            r, g, b = avg_color.astype(int)
            html.append(f'<span style="color:rgb({r},{g},{b})">{best_char}</span>')
        
        html.append('<br>')
    
    html.append('</pre>')
    return ''.join(html)
```

---

## 📄 示例 3: 添加 SVG 输出

### 步骤 1: 创建输出函数

```python
def output_svg(sampling_array, char_data, width=800, height=600):
    """生成 SVG 格式输出
    
    Args:
        sampling_array: 采样数组
        char_data: 字符数据
        width: SVG 宽度
        height: SVG 高度
    
    Returns:
        SVG 字符串
    """
    rows, cols = sampling_array.shape[:2]
    cell_w = width / cols
    cell_h = height / rows
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'width="{width}" height="{height}">']
    svg.append(f'<rect width="100%" height="100%" fill="black"/>')
    
    for row in range(rows):
        for col in range(cols):
            block = sampling_array[row, col]
            best_char = match_char(block, char_data)
            
            x = col * cell_w
            y = (row + 1) * cell_h
            
            svg.append(f'<text x="{x}" y="{y}" '
                      f'font-family="monospace" '
                      f'font-size="{cell_h}" '
                      f'fill="white">{best_char}</text>')
    
    svg.append('</svg>')
    return '\n'.join(svg)
```

---

### 步骤 2: 添加命令行选项

```python
p.add_argument('--format', 
               choices=['text', 'ansi', 'html', 'svg'],
               default='text',
               help='输出格式 (默认: text)')
```

---

### 步骤 3: 路由到不同输出函数

```python
if args.format == 'text':
    output = get_final_output(...)
elif args.format == 'ansi':
    output = output_ansi(...)
elif args.format == 'html':
    output = output_html(...)
elif args.format == 'svg':
    output = output_svg(...)
```

---

## 🔌 示例 4: 插件化架构（未来）

### 设计思路

```python
# plugins/matching_algorithms.py
class MatchingAlgorithm:
    """匹配算法基类"""
    
    def compute_score(self, block, char_matrix):
        raise NotImplementedError

class SADAlgorithm(MatchingAlgorithm):
    def compute_score(self, block, char_matrix):
        return np.sum(np.abs(block - char_matrix))

class SSDAlgorithm(MatchingAlgorithm):
    def compute_score(self, block, char_matrix):
        return np.sum((block - char_matrix) ** 2)
```

---

### 插件注册

```python
# plugins/__init__.py
ALGORITHMS = {
    'sad': SADAlgorithm(),
    'ssd': SSDAlgorithm(),
}

def register_algorithm(name, algo):
    ALGORITHMS[name] = algo
```

---

### 动态加载

```python
def get_final_output(..., algorithm_name='sad'):
    algo = ALGORITHMS.get(algorithm_name)
    if not algo:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    # 使用插件
    score = algo.compute_score(block, char_matrix)
```

---

## 📚 扩展最佳实践

### 1. 保持向后兼容

```python
# ✅ 提供默认值
def new_function(param1, param2, new_param=None):
    if new_param is None:
        new_param = DEFAULT_VALUE
    ...
```

---

### 2. 添加充分测试

- 单元测试覆盖新功能
- 性能回归测试
- 边界情况测试

---

### 3. 文档同步更新

- API 参考文档
- 用户指南
- 示例代码

---

### 4. 性能评估

```bash
# 对比新旧实现的性能
python tools/benchmark.py bench --image test.png --height 30
```

确保性能退化 < 10%

---

## 💡 常见扩展场景

### 场景 1: 添加新的插值算法

**位置**: `INTERPOLATION_MAP` in `constants.py`

**步骤**:
1. 查找 OpenCV 支持的插值算法
2. 添加到映射表
3. 更新文档

---

### 场景 2: 支持新的字体格式

**位置**: `get_baseimg()` and `_render_char_to_matrix()`

**步骤**:
1. 研究字体格式规范
2. 使用合适的库加载（如 fonttools）
3. 适配现有渲染流程

---

### 场景 3: 添加实时预览

**位置**: 新的模块 `realtime_preview.py`

**步骤**:
1. 使用 tkinter 或 PyQt 创建 GUI
2. 逐行输出而非等待全部完成
3. 提供暂停/继续控制

---

## 🎓 学习资源

- [架构设计](architecture.md) - 了解系统结构
- [API 参考](api-reference.md) - 查阅函数签名
- [代码规范](coding-standards.md) - 遵循编码标准
- [现有插件](../../tools/) - 参考可视化工具的实现

---

*最后更新: 2026-06-09*
