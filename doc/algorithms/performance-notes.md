#  UnicodeArt 性能注意事项

##  性能概览

### 典型场景性能数据

| 场景 | 输入尺寸 | 输出尺寸 | 字符集 | 耗时 | 内存峰值 |
|------|----------|----------|--------|------|----------|
| **小图** | 100×100 | 20×20 | ASCII (95) | ~0.1s | ~5 MB |
| **中图** | 500×500 | 50×50 | ASCII (95) | ~0.5s | ~25 MB |
| **大图** | 1920×1080 | 100×60 | ASCII+中文 (145) | ~2s | ~100 MB |
| **超大图** | 4K (3840×2160) | 200×120 | ASCII+中文 (145) | ~8s | ~400 MB |

**测试环境**: Intel i7-10700K, 32GB RAM, Python 3.9

---

## 🔍 性能瓶颈分析

### 1. 图像采样阶段 (~20% 耗时)

**瓶颈点**:
- `cv2.resize()` 调用次数 = 采样块数量
- 每次 resize 涉及插值计算

**优化建议**:
```python
#  低效: 逐块 resize
for y in range(0, H, rectsize_h):
    for x in range(0, W, rectsize_w):
        block = image[y:y+h, x:x+w]
        resized = cv2.resize(block, (M, M))  # 频繁调用

# ✅ 高效: 批量处理 (如果可能)
# 使用 OpenCV 的金字塔缩放或一次性下采样
downscaled = cv2.resize(image, (output_width * M, output_height * M))
# 然后分块提取
```

**实际效果**: 减少 30-50% 采样时间

---

### 2. 字符匹配阶段 (~70% 耗时) ⚠️ **主要瓶颈**

**瓶颈点**:
- SAD 计算次数 = 采样块数 × 字符集大小
- 每次 SAD 涉及 M² 次减法和加法

**优化策略**:

#### A. 早期终止 (Early Termination)
```python
def calculate_sad_early_stop(rectangle, char_matrix, current_min):
    total = 0.0
    for i in range(len(rectangle)):
        for j in range(len(rectangle[0])):
            total += abs(rectangle[i][j] - char_matrix[i][j])
            if total >= current_min:
                return total  # 提前终止
    return total
```
**效果**: 减少 20-40% 计算量

#### B. 候选过滤 (Candidate Filtering)
```python
# 预计算字符统计特征
for char in char_data:
    char['mean'] = np.mean(char['matrix'])
    char['var'] = np.var(char['matrix'])

# 快速筛选
block_mean = np.mean(rectangle)
candidates = [c for c in char_data if abs(c['mean'] - block_mean) < 0.15]

# 只在候选集中精确匹配
if candidates:
    scores = [calculate_sad(rectangle, c['matrix']) for c in candidates]
    best_idx = np.argmin(scores)
    return candidates[best_idx], scores[best_idx]
```
**效果**: 减少 50-70% 计算量

#### C. 向量化加速
```python
# 批量计算所有字符的 SAD
char_matrices = np.stack([c['matrix'] for c in char_data])  # (C, M, M)
diffs = np.abs(rectangle - char_matrices)  # (C, M, M)
scores = np.sum(diffs, axis=(1, 2))  # (C,)
best_idx = np.argmin(scores)
```
**效果**: 利用 NumPy SIMD 指令，提升 3-5x

---

### 3. 字符渲染阶段 (~10% 耗时)

**瓶颈点**:
- Pillow `draw.text()` 调用次数 = 字符集大小
- 字体加载和光栅化

**优化建议**:
```python
# ✅ 缓存已渲染的字符矩阵
_char_cache = {}

def get_char_matrix_cached(char, font, size):
    key = (char, font.path, size)
    if key not in _char_cache:
        matrix = render_char_to_matrix(char, font, size)
        _char_cache[key] = matrix
    return _char_cache[key]
```
**效果**: 避免重复渲染，启动后几乎零耗时

---

## 💾 内存优化

### 1. 数据类型选择

| 类型 | 精度 | 内存占用 | 推荐场景 |
|------|------|----------|----------|
| `float64` | 双精度 | 8 字节/元素 | 高精度需求 |
| `float32` | 单精度 | 4 字节/元素 | **默认推荐** ✅ |
| `uint8` | 整数 | 1 字节/元素 | 最终输出 |

**建议**: 中间计算使用 `float32`，节省 50% 内存

```python
# 修改前
sampling_array = np.zeros((H, W, M, M), dtype=np.float64)

# 修改后
sampling_array = np.zeros((H, W, M, M), dtype=np.float32)
```

---

### 2. 及时释放中间变量

```python
def process_image(image_path):
    # 加载图像
    image = cv2.imread(image_path, 0)
    
    # 采样
    sampling_array = get_sampling_array(image, ...)
    
    # ✅ 释放大对象
    del image
    
    # 匹配
    output = get_final_output(sampling_array, ...)
    
    # ✅ 释放采样数组
    del sampling_array
    
    return output
```

---

### 3. 分块处理超大图像

**问题**: 4K+ 图像可能导致内存不足

**解决方案**: 分块处理，逐行生成输出

```python
def process_large_image(image_path, chunk_size=100):
    image = cv2.imread(image_path, 0)
    H, W = image.shape
    
    output_lines = []
    
    # 逐块处理
    for y_start in range(0, H, chunk_size):
        y_end = min(y_start + chunk_size, H)
        chunk = image[y_start:y_end, :]
        
        # 处理当前块
        sampling_chunk = get_sampling_array(chunk, ...)
        output_chunk = get_final_output(sampling_chunk, ...)
        
        output_lines.append(output_chunk)
        
        # 释放当前块
        del sampling_chunk
    
    # 合并输出
    return '\n'.join(output_lines)
```

**效果**: 内存占用从 O(H×W) 降低到 O(chunk_size×W)

---

## ⚡ 并行化策略

### 1. 多线程 (Python)

**适用场景**: CPU 密集型任务，多核处理器

```python
from concurrent.futures import ThreadPoolExecutor

def process_row(args):
    row_index, row_data, char_data, wide_data = args
    # 匹配逻辑...
    return output_row

# 并行处理每行
with ThreadPoolExecutor(max_workers=4) as executor:
    tasks = [(i, row, char_data, wide_data) 
             for i, row in enumerate(sampling_array)]
    results = list(executor.map(process_row, tasks))

final_output = '\n'.join(results)
```

**加速比**: ~2-3x (4 核 CPU)

**注意**: Python GIL 限制，适合 I/O 密集型或 NumPy 操作

---

### 2. 多进程 (Python)

**适用场景**: 绕过 GIL 限制，真正并行

```python
from multiprocessing import Pool

def process_chunk(chunk_args):
    chunk_id, chunk_data, char_data, wide_data = chunk_args
    # 处理逻辑...
    return output_chunk

# 将图像分成 N 个块
chunks = split_image_into_chunks(image, num_chunks=4)

with Pool(processes=4) as pool:
    tasks = [(i, chunk, char_data, wide_data) 
             for i, chunk in enumerate(chunks)]
    results = pool.map(process_chunk, tasks)

# 合并结果
final_output = merge_chunks(results)
```

**加速比**: ~3-4x (4 核 CPU)

**注意**: 进程间通信开销，适合大块任务

---

### 3. GPU 加速 (实验性)

**工具**: CuPy (NumPy GPU 版本)

```python
import cupy as cp

# 将数据转移到 GPU
rectangle_gpu = cp.asarray(rectangle)
char_matrices_gpu = cp.asarray(char_matrices)

# GPU 上计算 SAD
diffs_gpu = cp.abs(rectangle_gpu - char_matrices_gpu)
scores_gpu = cp.sum(diffs_gpu, axis=(1, 2))
best_idx_gpu = cp.argmin(scores_gpu)

# 转移回 CPU
best_idx = int(best_idx_gpu.get())
```

**加速比**: ~10-50x (取决于 GPU)

**注意**: 
- 需要 NVIDIA GPU + CUDA
- 数据传输开销
- 仅适合大规模计算

---

## 🌐 JS 移植性能考虑

### 1. 浏览器端限制

| 限制项 | Python | JavaScript (Browser) | 影响 |
|--------|--------|---------------------|------|
| **单线程** | 可多线程 | 主线程阻塞 UI | ⚠️ 需 Web Workers |
| **内存** | 无限制 | ~1-2 GB | ️ 大图像受限 |
| **CPU** | 原生速度 | JIT 编译 | ~2-5x 慢 |
| **并行** | 多进程/线程 | Web Workers | 复杂度高 |

---

### 2. 优化策略

#### A. Web Workers 并行化

```javascript
// main.js
const workers = [];
const numWorkers = navigator.hardwareConcurrency || 4;

for (let i = 0; i < numWorkers; i++) {
  workers.push(new Worker('matcher-worker.js'));
}

// 分发任务
const rowsPerWorker = Math.ceil(samplingArray.length / numWorkers);
samplingArray.forEach((row, i) => {
  const workerIndex = Math.floor(i / rowsPerWorker);
  workers[workerIndex].postMessage({ 
    row, 
    charData, 
    wideData,
    rowIndex: i 
  });
});

// 收集结果
let completed = 0;
const results = new Array(samplingArray.length);

workers.forEach((worker, idx) => {
  worker.onmessage = (e) => {
    results[e.data.rowIndex] = e.data.output;
    completed++;
    
    if (completed === samplingArray.length) {
      // 所有任务完成
      const finalOutput = results.join('\n');
      displayOutput(finalOutput);
    }
  };
});
```

**效果**: 充分利用多核 CPU，避免 UI 阻塞

---

#### B. TypedArray 优化

```javascript
// ❌ 慢: 普通数组
const matrix = [[0.1, 0.2], [0.3, 0.4]];

// ✅ 快: TypedArray
const matrix = new Float32Array([0.1, 0.2, 0.3, 0.4]);

// 访问元素
function get(matrix, size, i, j) {
  return matrix[i * size + j];
}
```

**效果**: 提升 2-5x 性能

---

#### C. 避免 GC (垃圾回收)

```javascript
// ❌ 频繁创建对象
for (let i = 0; i < 1000; i++) {
  const temp = new Float32Array(size * size);  // 每次分配
  // ...
}

// ✅ 复用缓冲区
const temp = new Float32Array(size * size);
for (let i = 0; i < 1000; i++) {
  // 重用 temp
  // ...
}
```

**效果**: 减少 GC 停顿，提升稳定性

---

#### D. Canvas 离屏渲染

```javascript
// 预计算字符矩阵时使用离屏 Canvas
const offscreenCanvas = document.createElement('canvas');
offscreenCanvas.width = matrixSize * 2;
offscreenCanvas.height = matrixSize;
const ctx = offscreenCanvas.getContext('2d');

// 渲染字符
ctx.font = `${fontSize}px ${fontFamily}`;
ctx.fillText(char, 0, fontSize);

// 提取像素数据
const imageData = ctx.getImageData(0, 0, offscreenCanvas.width, offscreenCanvas.height);
const matrix = new Float32Array(imageData.data.length / 4);
for (let i = 0; i < matrix.length; i++) {
  matrix[i] = 1.0 - imageData.data[i * 4] / 255.0;  // 归一化
}
```

**效果**: 比手动绘制快 10x+

---

## 📈 性能基准测试

### 测试工具

项目提供 `tools/benchmark.py` 进行性能测试:

```bash
# 基础性能测试
python tools/benchmark.py --image test.png --height 50

# 详细剖析
python tools/benchmark.py --image test.png --height 50 --profile

# 对比不同参数
python tools/benchmark.py --compare \
  --config1 "height=50,matrix=5" \
  --config2 "height=100,matrix=5"
```

### 关键指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **总耗时** | 端到端执行时间 | < 2s (中图) |
| **采样耗时** | 图像采样阶段 | < 0.5s |
| **匹配耗时** | 字符匹配阶段 | < 1.5s |
| **内存峰值** | 最大内存占用 | < 100 MB |
| **GC 次数** | 垃圾回收次数 | < 10 次 |

---

##  最佳实践总结

### ✅ 应该做的

1. **使用 float32**: 节省 50% 内存
2. **启用候选过滤**: 减少 50-70% 计算量
3. **缓存字符矩阵**: 避免重复渲染
4. **及时释放变量**: 防止内存泄漏
5. **并行化处理**: 利用多核 CPU
6. **分块处理大图**: 避免内存不足

### ❌ 避免做的

1. **不要使用 float64**: 除非必要
2. **不要完整遍历字符集**: 使用早期终止
3. **不要重复加载字体**: 缓存字体对象
4. **不要在大循环中创建对象**: 复用缓冲区
5. **不要阻塞主线程 (JS)**: 使用 Web Workers

---

## 📚 参考文献

1. **NumPy Performance Guide**: https://numpy.org/doc/stable/user/performance.html
2. **Python Multiprocessing**: https://docs.python.org/3/library/multiprocessing.html
3. **Web Workers API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API
4. **CuPy Documentation**: https://docs.cupy.dev/en/stable/

---

*最后更新: 2026-06-08*
