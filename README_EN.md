# 🎨 UnicodeArt

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPLv3-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/unicodeart.svg)](https://pypi.org/project/unicodeart/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](doc/README.md)

> **Project Positioning**: Unicode character art generator
> **Core Goal**: Focus on **algorithm clarity**, **logical readability**, and **architectural portability**

This project is improved based on [asciifier](https://github.com/yutotakano/asciifier):

- ✅ Optimized program structure and code readability
- ✅ Enhanced wide character (Chinese/Japanese) support
- ✅ Improved parameter configuration and error handling
- ✅ Complete documentation system

---

## 🚀 Quick Start

### Installation

**Method 1: Install from PyPI (Recommended)**

```bash
pip install unicodeart
```

**Method 2: Install from Source**

```bash
git clone https://github.com/your-username/UnicodeArt.git
cd UnicodeArt
pip install -r requirements.txt
```

**Detailed Installation Guide**: [📦 Installation Instructions](doc/users/installation.en.md)

---

### Basic Usage

#### Text to ASCII Art

```bash
python unicodeart.py -t "Hello" --font "C:\Windows\Fonts\SimSun.ttc" --height 15
```

#### Image to ASCII Art

```bash
python unicodeart.py -i photo.jpg --height 30 -o output.txt
```

**5-Minute Quick Start**: [🚀 Quick Start Tutorial](doc/users/quick-start.en.md)

---

## 📚 Documentation Navigation

### 👥 User Documentation

- [📦 Installation Guide](doc/users/installation.en.md) - Environment setup and dependency installation
- [🚀 Quick Start](doc/users/quick-start.en.md) - Get started in 5 minutes
- [📚 Feature Details](doc/users/features.en.md) - Detailed explanation of all parameters
- [❓ FAQ](doc/users/faq.en.md) - Frequently asked questions and troubleshooting
- [📖 Usage Examples](doc/users/examples/)
  - [Basic Usage](doc/users/examples/basic-usage.en.md)
  - [Custom Character Sets](doc/users/examples/custom-chars.en.md)
  - [Wide Character Demo](doc/users/examples/wide-char-demo.en.md)
  - [Advanced Options](doc/users/examples/advanced-options.en.md)

---

### 👨‍💻 Developer Documentation

- [🏗️ Architecture Design](doc/devs/architecture.en.md) - Module division and data flow
- [📖 API Reference](doc/devs/api-reference.en.md) - Function signatures and usage examples
- [📝 Coding Standards](doc/devs/coding-standards.en.md) - Coding standards and best practices
- [🤝 Contributing Guide](doc/devs/contributing.en.md) - How to submit PRs
- [🚀 Extension Development](doc/devs/extending.en.md) - How to add new features

---

### 🔬 Algorithm Documentation

- [📊 Algorithm Overview](doc/algorithms/README.en.md) - Core algorithm overview
- [🖼️ Image to Art](doc/algorithms/image-to-art.en.md) - Detailed algorithm flow
- [📝 Text to Art](doc/algorithms/text-to-art.en.md) - Text rendering principles
- [🔤 Character Matching](doc/algorithms/character-matching.en.md) - SAD algorithm details
- [🌏 Wide Character Handling](doc/algorithms/wide-character-handling.en.md) - Dual character set mechanism
- [⚡ Performance Analysis](doc/algorithms/performance-notes.en.md) - Complexity analysis and optimization

---

## 🛠️ Toolset

### Algorithm Visualization Tool

```bash
python tools/visualizer.py --image test.png --height 20 --output-dir viz_output
```

Generates:

- Sampling grid overlay
- Character matrix heatmap
- HTML step-by-step execution report

---

### Performance Benchmarking

```bash
python tools/benchmark.py bench --image test.png --height 30
```

Outputs:

- Stage-by-stage timing
- Peak memory usage
- Markdown/JSON reports

---

## ⚙️ Command Line Parameters

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

**Complete Parameter Description**: [📚 Feature Details](doc/users/features.en.md)

### Common Parameters Quick Reference

| Parameter           | Description             | Default          |
| ------------------- | ----------------------- | ---------------- |
| `-i, --image`     | Input image path        | -                |
| `-t, --text`      | Input text              | -                |
| `-o, --output`    | Output file             | stdout           |
| `--height`        | Output height           | -                |
| `--font`          | Font path               | -                |
| `--chars`         | Character set           | `" .:-=+*#%@"` |
| `--ratio`         | Height-to-width ratio   | `2.0`          |
| `--matrix`        | Sampling matrix size    | `6`            |
| `--interpolation` | Interpolation algorithm | `bilinear`     |

---

## 🎯 Typical Use Cases

### Terminal Quick Preview

```bash
python unicodeart.py -i photo.jpg --height 20 --matrix 4 --chars " ░▒▓█"
```

### Social Media Sharing

```bash
python unicodeart.py -i photo.jpg --height 50 -o output.txt
```

### High-Quality Printing

```bash
python unicodeart.py -i photo.jpg --height 100 --matrix 8 \
  --chars " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" \
  -o output.txt
```

### Chinese Text Banner

```bash
python unicodeart.py -t "你好世界" \
  --font "C:\Windows\Fonts\SimSun.ttc" \
  --height 20
```

**Note**:

- Default `--ratio=2.0` is the standard value, no need to specify
- In mixed monospaced font environments (VSCode, modern terminals), this is the only correct configuration

**More Examples**: [📖 Usage Example Collection](doc/users/examples/)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Generate HTML report
pytest --html=tests/report.html

# Run specific tests
pytest tests/test_character_matching.py -v
```

---

## 📊 Performance Characteristics

| Configuration          | Relative Speed | Use Case                |
| ---------------------- | -------------- | ----------------------- |
| `matrix=4, nearest`  | ⚡⚡⚡⚡⚡     | Real-time preview       |
| `matrix=6, bilinear` | ⚡⚡⚡⚡       | Daily use (recommended) |
| `matrix=8, bicubic`  | ⚡⚡⚡         | High quality            |
| `matrix=10, lanczos` | ⚡⚡           | Print output            |

**Detailed Performance Analysis**: [⚡ Performance Notes](doc/algorithms/performance-notes.en.md)

---

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

**Contributing Guide**: [🤝 How to Contribute](doc/devs/contributing.en.md)

---

## 📄 License

GNU GPL v3 License

---

## 🔗 Related Links

- **[asciifier](https://github.com/yutotakano/asciifier)** - Original project

---

## 🌐 Multi-language Support

- [🇺🇸 English Documentation](README_EN.md) (current)
- [🇨🇳 中文文档](README.md)

---

*Last updated: 2026-06-09*
