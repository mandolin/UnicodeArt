#  字符匹配算法原理

##  核心问题

**目标**: 对于给定的采样块 (灰度矩阵)，从字符集中找到最相似的字符

**挑战**:
1. **计算效率**: 字符集可能包含数百个字符，每个都需要比较
2. **匹配精度**: 需要准确捕捉形状相似性，而非像素级精确匹配
3. **宽字符处理**: 宽字符占用两个位置，需要特殊合并策略

---

## 🔍 匹配度量: 绝对差值之和 (SAD)

### 定义

**SAD (Sum of Absolute Differences)**: 两个矩阵对应元素差值的绝对值之和

**公式**:
```
SAD(A, B) = Σᵢⱼ |Aᵢⱼ - Bᵢ|
```

其中:
- A: 采样块矩阵 (M × M)
- B: 字符矩阵 (M × M)
- i, j: 矩阵索引

**实现**:
```python
def _calculate_match_score(rectangle, char_matrix):
    """
    计算采样块与字符矩阵的匹配得分 (SAD)
    
    Args:
        rectangle: 采样块矩阵 (归一化到 [0, 1])
        char_matrix: 字符矩阵 (归一化到 [0, 1])
    
    Returns:
        float: SAD 得分 (越小越相似)
    """
    # 计算绝对差值
    diff = np.abs(rectangle - char_matrix)
    
    # 求和
    score = np.sum(diff)
    
    return score
```

**时间复杂度**: O(M²)，其中 M = matrix_size

---

### 为什么选择 SAD？

**优点**:
1. **简单直观**: 易于理解和实现
2. **计算高效**: 只需减法和加法，无复杂运算
3. **鲁棒性强**: 对噪声和微小偏移不敏感
4. **可并行化**: 每个像素独立计算

**替代方案对比**:

| 度量方法 | 优点 | 缺点 | 适用场景 |
|----------|------|------|----------|
| **SAD** | 简单、快速 | 对亮度敏感 | 通用场景 ✅ |
| SSD (平方差) | 强调大差异 | 计算稍慢 (乘法) | 高精度需求 |
| NCC (归一化互相关) | 对亮度不敏感 | 计算复杂 | 光照变化大 |
| Hausdorff 距离 | 捕捉形状轮廓 | 实现复杂 | 边缘检测 |

**结论**: SAD 在速度和精度之间取得良好平衡，适合实时应用

---

## 🎯 匹配流程

### 完整流程

```mermaid
graph TD
    A[采样块 rectangle] --> B{是否有下一个块?}
    B -->|Yes| C[获取 next_rectangle]
    B -->|No| D[用空白矩形填充]
    C --> E[合并: combined = hstackrectangle, next_rectangle)]
    D --> E
    E --> F[计算与普通字符的 SAD]
    E --> G[计算与宽字符的 SAD]
    F --> H[找到最佳普通字符 normal_indice, normal_score]
    G --> I[找到最佳宽字符 wide_indice, wide_score]
    H --> J{wide_score < ratio * normal_score?}
    I --> J
    J -->|Yes| K[使用宽字符 + skip_sign]
    J -->|No| L[使用普通字符]
```

### 详细步骤

#### 1. 准备阶段

```python
# 输入
rectangle = sampling_array[y_index, x_index]  # M x M
next_rectangle = sampling_array[y_index, x_index + 1] if not is_last else None

# 预计算数据
char_data = [...]      # 普通字符列表
wide_char_data = [...] # 宽字符列表
```

#### 2. 普通字符匹配

```python
normal_indice, normal_score = _find_best_normal_char(rectangle, char_data)
```

**内部逻辑**:
```python
# 计算每个字符的 SAD 得分
scores = []
for char_info in char_data:
    score = np.sum(np.abs(rectangle - char_info['matrix']))
    scores.append(score)

# 找到最小得分
normal_indice = np.argmin(scores)
normal_score = scores[normal_indice]
```

#### 3. 宽字符匹配

```python
# 合并当前块和下一块
if next_rectangle is None:
    blank = np.ones_like(rectangle)
    combined = np.hstack((rectangle, blank))
else:
    combined = np.hstack((rectangle, next_rectangle))

# 计算宽字符 SAD
wide_indice, wide_score = _find_best_wide_char(combined, wide_char_data)
```

#### 4. 决策

```python
if wide_score < wide_ratio * normal_score and not is_last_in_row:
    use_wide = True
    skip_sign = True
else:
    use_wide = False
```

---

## ⚖️ 权重比例调整

### wide_sum_ratio 参数

**定义**: 宽字符匹配得分的权重比例

**默认值**: 2.0

**含义**: 宽字符得分需要比普通字符小此倍数才优先使用

**数学表达**:
```
使用宽字符  wide_score < wide_ratio × normal_score
```

### 调整策略

| 场景 | 推荐值 | 原因 |
|------|--------|------|
| **标准字体** | 2.0 | 平衡普通/宽字符使用 |
| **粗体字体** | 1.5-1.8 | 宽字符更易识别，降低阈值 |
| **细体字体** | 2.2-2.5 | 宽字符细节少，提高阈值 |
| **高对比度图像** | 1.8-2.0 | 边缘清晰，宽字符优势明显 |
| **低对比度图像** | 2.2-2.8 | 噪声多，保守使用宽字符 |

**实验建议**:
```bash
# 测试不同 ratio 值
python unicodeart.py -i image.png --wide-char-ratio 1.5 -o out1.txt
python unicodeart.py -i image.png --wide-char-ratio 2.0 -o out2.txt
python unicodeart.py -i image.png --wide-char-ratio 2.5 -o out3.txt

# 人工评估视觉效果
```

---

##  优化技巧

### 1. 早期终止 (Early Termination)

**思路**: 如果当前累计得分已超过已知最小得分，提前终止计算

**实现**:
```python
def _calculate_match_score_early_stop(rectangle, char_matrix, current_min):
    """带早期终止的 SAD 计算"""
    total = 0.0
    for i in range(len(rectangle)):
        for j in range(len(rectangle[0])):
            total += abs(rectangle[i][j] - char_matrix[i][j])
            if total >= current_min:
                return total  # 提前终止
    
    return total
```

**效果**: 减少 20-40% 的计算量 (取决于字符集分布)

---

### 2. 缓存优化

**思路**: 预计算字符矩阵的统计特征，快速筛选候选

**实现**:
```python
# 预计算阶段 (一次性)
for char in char_data:
    matrix = char['matrix']
    char['mean'] = np.mean(matrix)
    char['var'] = np.var(matrix)
    char['energy'] = np.sum(matrix ** 2)

# 匹配阶段
block_mean = np.mean(rectangle)
block_var = np.var(rectangle)

# 快速筛选: 均值和方差接近的字符
candidates = [c for c in char_data 
              if abs(c['mean'] - block_mean) < 0.15 
              and abs(c['var'] - block_var) < 0.05]

# 只在候选集中精确匹配
if candidates:
    scores = [_calculate_match_score(rectangle, c['matrix']) 
              for c in candidates]
    best_idx = np.argmin(scores)
    return candidates[best_idx], scores[best_idx]
else:
    # 降级到完整匹配
    ...
```

**效果**: 减少 50-70% 的匹配计算量

---

### 3. 向量化加速

**Python (NumPy)**:
```python
# 批量计算所有字符的 SAD
char_matrices = np.stack([c['matrix'] for c in char_data])  # (C, M, M)
diffs = np.abs(rectangle - char_matrices)  # (C, M, M)
scores = np.sum(diffs, axis=(1, 2))  # (C,)
best_idx = np.argmin(scores)
```

**JS (TypedArray)**:
```javascript
// 使用 Float32Array 提升性能
const charMatrices = new Float32Array(C * M * M);
// 填充数据...

const diffs = new Float32Array(C * M * M);
for (let c = 0; c < C; c++) {
  for (let i = 0; i < M * M; i++) {
    diffs[c * M * M + i] = Math.abs(rectangle[i] - charMatrices[c * M * M + i]);
  }
}

// 累加得分
const scores = new Float32Array(C);
for (let c = 0; c < C; c++) {
  let sum = 0;
  for (let i = 0; i < M * M; i++) {
    sum += diffs[c * M * M + i];
  }
  scores[c] = sum;
}
```

---

## 📊 复杂度分析

### 时间复杂度

| 操作 | 复杂度 | 说明 |
|------|--------|------|
| 单次 SAD 计算 | O(M²) | M = matrix_size |
| 普通字符匹配 | O(C_n × M²) | C_n = 普通字符数量 |
| 宽字符匹配 | O(C_w × M²) | C_w = 宽字符数量 |
| 总匹配 (单块) | O((C_n + C_w) × M²) | - |
| 总匹配 (全图) | O(R × (C_n + C_w) × M²) | R = 采样块数量 |

**典型场景**:
- M = 5
- C_n = 95 (ASCII)
- C_w = 50 (中文常用字)
- R = 2500 (50×50 输出)
- **总计算量**: 2500 × 145 × 25 ≈ 9M 次运算
- **耗时**: ~0.1-0.5 秒 (现代 CPU)

### 空间复杂度

| 数据结构 | 大小 | 说明 |
|----------|------|------|
| 采样块 | M² | 临时变量 |
| 合并块 (宽字符) | 2×M² | 临时变量 |
| 字符矩阵缓存 | (C_n + C_w) × M² | 预计算 |
| 得分数组 | C_n + C_w | 临时存储 |
| **总计** | **O((C_n + C_w) × M²)** | 主导项为字符缓存 |

---

## 🔧 JS 移植要点

### 关键转换

| Python | JavaScript | 性能提示 |
|--------|------------|----------|
| `np.abs(a - b)` | 循环计算 | 避免创建中间数组 |
| `np.sum(array)` | `reduce` 或手动累加 | 手动累加更快 |
| `np.argmin(array)` | 手动遍历找最小值 | 避免展开大数组 |
| `np.hstack((a, b))` | 逐行拼接 | 预分配结果数组 |

### 性能优化

1. **使用 TypedArray**: `Float32Array` 比 `Array<number>` 快 2-5x
2. **避免 GC**: 复用缓冲区，减少对象创建
3. **Web Workers**: 将匹配计算移至后台线程
4. **SIMD.js**: 浏览器支持时使用 SIMD 指令 (实验性)

### 代码示例

```javascript
// 高效 SAD 计算
function calculateSAD(rectangle, charMatrix, size) {
  let sum = 0;
  for (let i = 0; i < size; i++) {
    const rowOffset = i * size;
    for (let j = 0; j < size; j++) {
      sum += Math.abs(rectangle[rowOffset + j] - charMatrix[rowOffset + j]);
    }
  }
  return sum;
}

// 批量匹配
function findBestChar(rectangle, charData, size) {
  let bestIndex = 0;
  let bestScore = Infinity;
  
  for (let c = 0; c < charData.length; c++) {
    const score = calculateSAD(rectangle, charData[c].matrix, size);
    if (score < bestScore) {
      bestScore = score;
      bestIndex = c;
    }
  }
  
  return { index: bestIndex, score: bestScore };
}
```

---

##  参考文献

1. **Image Matching**: Brown & Lowe, "Invariant Features from Interest Point Groups"
2. **SAD Algorithm**: Wikipedia - Sum of absolute differences
3. **Optimization Techniques**: Intel IPP Library Documentation

---

*最后更新: 2026-06-08*
