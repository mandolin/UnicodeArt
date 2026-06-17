# 🎨 UnicodeArt

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPLv3-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/unicodeart.svg)](https://pypi.org/project/unicodeart/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](doc/README.md)

> **项目定位**: unicode字符画生成程序
> **核心目标**: 专注于**算法清晰度**、**逻辑可读性**、**架构可移植性**

本项目基于 [asciifier](https://github.com/yutotakano/asciifier) 进行了改进：

- ✅ 优化程序结构和代码可读性
- ✅ 增强宽字符（中文/日文等）支持
- ✅ 完善参数配置和错误处理
- ✅ 提供完整的文档体系

---

## 🚀 快速开始

### 安装

**方式 1: 从 PyPI 安装（推荐）**

```bash
pip install unicodeart
```

**方式 2: 从源码安装**

```bash
git clone https://github.com/your-username/UnicodeArt.git
cd UnicodeArt
pip install -r requirements.txt
```

**详细安装指南**: [📦 安装说明](doc/users/installation.md)

---

### 基础用法

#### 文本转字符画

```bash
python unicodeart.py -t "Hello" --font "C:\Windows\Fonts\SimSun.ttc" --height 15
```

#### 图片转字符画

```bash
python unicodeart.py -i photo.jpg --height 30 -o output.txt
```

**5分钟快速入门**: [🚀 快速入门教程](doc/users/quick-start.md)

---

## 📚 文档导航

### 👥 用户文档

- [📦 安装指南](doc/users/installation.md) - 环境配置和依赖安装
- [🚀 快速入门](doc/users/quick-start.md) - 5分钟上手
- [📚 功能详解](doc/users/features.md) - 所有参数详细说明
- [❓ 常见问题](doc/users/faq.md) - FAQ 和故障排查
- [📖 使用示例](doc/users/examples/)
  - [基础用法](doc/users/examples/basic-usage.md)
  - [自定义字符集](doc/users/examples/custom-chars.md)
  - [宽字符演示](doc/users/examples/wide-char-demo.md)
  - [高级选项](doc/users/examples/advanced-options.md)

---

### 👨‍💻 开发者文档

- [🏗️ 架构设计](doc/devs/architecture.md) - 模块划分和数据流
- [📖 API 参考](doc/devs/api-reference.md) - 函数签名和使用示例
- [📝 代码规范](doc/devs/coding-standards.md) - 编码标准和最佳实践
- [🤝 贡献指南](doc/devs/contributing.md) - 如何提交 PR
- [🚀 扩展开发](doc/devs/extending.md) - 如何添加新功能

---

### 🔬 算法文档

- [📊 算法总览](doc/algorithms/README.md) - 核心算法概览
- [🖼️ 图片转字符画](doc/algorithms/image-to-art.md) - 详细算法流程
- [📝 文本转字符画](doc/algorithms/text-to-art.md) - 文本渲染原理
- [🔤 字符匹配](doc/algorithms/character-matching.md) - SAD 算法详解
- [🌏 宽字符处理](doc/algorithms/wide-character-handling.md) - 双字符集机制
- [⚡ 性能分析](doc/algorithms/performance-notes.md) - 复杂度分析和优化

---

## 🛠️ 工具集

### 算法可视化工具

```bash
python tools/visualizer.py --image test.png --height 20 --output-dir viz_output
```

生成：

- 采样网格 overlay
- 字符矩阵热力图
- HTML 逐步执行报告

---

### 性能基准测试

```bash
python tools/benchmark.py bench --image test.png --height 30
```

输出：

- 各阶段耗时
- 内存峰值
- Markdown/JSON 报告

---

## ⚙️ 命令行参数

```bash
python unicodeart.py [-h] (-i IMAGE | -t TEXT) [-o OUTPUT] 
                     [--height HEIGHT] [--width WIDTH] 
                     [--font FONT] [--chars CHARS] 
                     [--ratio RATIO] [--matrix MATRIX]
                     [--font-style STYLE] [--font-reduce N]
                     [--interpolation ALGO] [--wide-char-ratio N]
                     [--height-mode MODE] [--line-spacing N]
                     [--invert] [--debug TAGS]
```

**完整参数说明**: [📚 功能详解](doc/users/features.md)

### 常用参数速查

| 参数                | 说明         | 默认值           |
| ------------------- | ------------ | ---------------- |
| `-i, --image`     | 输入图片路径 | -                |
| `-t, --text`      | 输入文本     | -                |
| `-o, --output`    | 输出文件     | stdout           |
| `--height`        | 输出高度     | -                |
| `--font`          | 字体路径     | -                |
| `--chars`         | 字符集       | `" .:-=+*#%@"` |
| `--ratio`         | 高宽比       | `2.0`          |
| `--matrix`        | 采样矩阵大小 | `6`            |
| `--interpolation` | 插值算法     | `bilinear`     |

---

## 🎯 典型用例

### 终端快速预览

```bash
python unicodeart.py -i photo.jpg --height 20 --matrix 4 --chars " ░▒▓█"
```

### 社交媒体分享

```bash
python unicodeart.py -i photo.jpg --height 50 -o output.txt
```

### 高质量打印

```bash
python unicodeart.py -i photo.jpg --height 100 --matrix 8 \
  --chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" \
  -o output.txt
```

### 中文文本 Banner

```bash
python unicodeart.py -t "你好世界" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 20
```

**说明**:

- 默认 `--ratio=2.0` 是标准值，无需指定
- 在混合等宽字体环境中（VSCode、现代终端），这是唯一正确配置

**更多示例**: [📖 使用示例集](doc/users/examples/)

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 生成 HTML 报告
pytest --html=tests/report.html

# 运行特定测试
pytest tests/test_character_matching.py -v
```

---

## 📊 性能特征

| 配置                   | 相对速度   | 适用场景         |
| ---------------------- | ---------- | ---------------- |
| `matrix=4, nearest`  | ⚡⚡⚡⚡⚡ | 实时预览         |
| `matrix=6, bilinear` | ⚡⚡⚡⚡   | 日常使用（推荐） |
| `matrix=8, bicubic`  | ⚡⚡⚡     | 高质量           |
| `matrix=10, lanczos` | ⚡⚡       | 打印输出         |

**详细性能分析**: [⚡ 性能注意事项](doc/algorithms/performance-notes.md)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**贡献指南**: [🤝 如何贡献](doc/devs/contributing.md)

---

## 📄 许可证

GNU GPL v3 License

---

## 🔗 相关链接

- **[asciifier](https://github.com/yutotakano/asciifier)** - 原始项目

---

## 🌐 多语言支持

- [🇨🇳 中文文档](README.md)（当前）
- [English Documentation](README_EN.md)

---

*最后更新: 2026-06-09*
