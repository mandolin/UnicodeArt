#  UnicodeArt 算法文档

##  文档说明

本目录包含 **UnicodeArt** 项目的核心算法详细说明，面向开发者和二次开发者。

---

##  文档列表

### [图片转字符画算法](image-to-art.md)
- 图像预处理流程
- 网格划分策略
- 采样矩阵生成
- 时间/空间复杂度分析

### [文本转字符画算法](text-to-art.md)
- 文本渲染机制
- 多行文本处理
- 字体加载与样式
- 对齐方式实现

### [字符匹配算法](character-matching.md)
- 绝对差值之和 (SAD) 原理
- 普通字符 vs 宽字符匹配
- 权重比例调整
- 优化思路

### [宽字符处理机制](wide-character-handling.md)
- 宽字符识别规则
- 双字符集架构
- 合并相邻矩形策略
- 边界情况处理

### [性能注意事项](performance-notes.md)
- 关键性能瓶颈
- 内存使用优化
- NumPy 向量化技巧
- JS 移植性能考虑

---

## 🎯 快速开始

### 对于 Python 开发者
1. 阅读 [图片转字符画算法](image-to-art.md) 了解整体流程
2. 查看 [字符匹配算法](character-matching.md) 理解核心逻辑
3. 参考 [性能注意事项](performance-notes.md) 优化代码

### 对于 JS 移植开发者
> **注意**: 详细的 JS 移植指南请在 **unicodeartjs** 项目中查看

1. 阅读各算法文档中的 **"JS 实现要点"** 章节
2. 关注 NumPy → JavaScript 的转换注意事项
3. 参考 [unicodeartjs/docs/code-mapping.md](link-to-js-repo) 获取详细对照表

---

## 🔗 相关资源

- [项目 README](../../README.md)
- [开发路线图](../../dev/roadmap.md)
- [JS 移植入口](../porting/README.md)

---

*最后更新: 2026-06-08*
