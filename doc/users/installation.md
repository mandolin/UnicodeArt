# 📦 安装指南

本指南将帮助你在本地环境中安装和配置 UnicodeArt。

---

## 🖥️ 系统要求

- **Python**: 3.8 或更高版本（推荐 3.10+）
- **操作系统**: Windows / macOS / Linux
- **内存**: 至少 512MB 可用内存
- **存储空间**: 至少 100MB（包含依赖库）

---

## 🔧 安装步骤

### 1. 克隆项目仓库

```bash
git clone https://github.com/your-username/UnicodeArt.git
cd UnicodeArt
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖库

```bash
pip install -r requirements.txt
```

**主要依赖说明**:
- `numpy`: 矩阵运算和图像处理
- `opencv-python`: 图像读取和处理
- `Pillow`: 字体渲染和图像生成
- `ConfigArgParse`: 命令行参数解析
- `pytest`: 单元测试框架（可选，用于运行测试）

### 4. 准备字体文件

**Windows 用户**:
- 系统自带字体位于 `C:\Windows\Fonts\`
- 推荐使用：
  - 宋体: `SimSun.ttc` 或 `simsun.ttc`
  - 微软雅黑: `MSYH.TTC`
  - 等宽字体: `consola.ttf`

**macOS 用户**:
- 系统字体位于 `/Library/Fonts/` 或 `~/Library/Fonts/`
- 推荐使用：
  - PingFang SC (苹方)
  - STHeiti (华文黑体)

**Linux 用户**:
- 安装中文字体包:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei
  
  # CentOS/RHEL
  sudo yum install wqy-zenhei-fonts wqy-microhei-fonts
  ```
- 字体路径通常在 `/usr/share/fonts/`

---

## ✅ 验证安装

运行以下命令验证安装是否成功：

```bash
# 查看帮助信息
python unicodeart.py --help

# 快速测试（文本模式）
python unicodeart.py -t "Hello" --font "C:\Windows\Fonts\SimSun.ttc" --height 10

# 如果有测试图片
python unicodeart.py -i test.png --height 20
```

**预期输出**:
- 帮助信息应显示所有可用参数
- 文本模式应在终端输出字符画
- 无错误提示

---

## ⚠️ 常见问题

### 问题 1: `ModuleNotFoundError: No module named 'cv2'`

**原因**: OpenCV 未正确安装

**解决**:
```bash
pip uninstall opencv-python
pip install opencv-python
```

### 问题 2: `OSError: cannot open resource`

**原因**: 字体文件路径错误或字体不存在

**解决**:
1. 确认字体文件存在
2. 使用绝对路径
3. Windows 用户注意路径分隔符使用 `\` 或转义 `\\`

```bash
# 正确示例
--font "C:\Windows\Fonts\SimSun.ttc"
--font "C:/Windows/Fonts/SimSun.ttc"
```

### 问题 3: `UnicodeDecodeError`

**原因**: 尝试用文本模式读取二进制文件

**解决**:
- 确保使用 `-i` 或 `--image` 参数加载图片
- 不要对图片文件使用 `@filename` 语法

### 问题 4: 中文字符显示为方块或乱码

**原因**: 字体不支持中文或编码问题

**解决**:
1. 使用支持中文的字体（如宋体、微软雅黑）
2. 确保终端支持 UTF-8 编码

```bash
# Windows PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Linux/macOS
export LANG=en_US.UTF-8
```

---

## 🎯 下一步

安装完成后，请阅读：
- 📖 [快速入门教程](quick-start.md) - 5分钟上手
- 📚 [功能详细说明](features.md) - 了解所有参数
- ❓ [常见问题解答](faq.md) - 解决问题

---

*最后更新: 2026-06-09*
