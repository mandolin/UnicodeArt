"""
UnicodeArt 常量配置模块

定义项目中使用的各种常量值,避免硬编码。
"""

#region 🟦 默认参数值

# 字体边缘预留空白像素 (避免字体过于接近图像边缘)
DEFAULT_FONT_REDUCE = 0

# 宽字符匹配得分的权重比例
# 含义: 宽字符的匹配得分需要比普通字符最小得分小此倍数才优先使用宽字符
DEFAULT_WIDE_CHAR_RATIO = 2.0

# 采样矩阵大小 (单个字符图像的归一化尺寸)
# ⚠️ 注意: 此值会影响采样精度和宽高比准确性
# - 推荐值: 6 (在 ratio=2.0 时能精确保持 2:1 比例,无取整误差)
# - 避免值: 5 (会导致 rectsize_w 从 2.5 向下取整为 2,产生 20% 比例失真)
DEFAULT_MATRIX_SIZE = 6

# 字符垂直与水平比例 (通常字体高度约为宽度的2倍)
# ⚠️ 注意: 此参数控制普通字符(英文/数字)的画布比例
# - 默认值 2.0: 适合大多数等宽英文字体(高度 ≈ 2×宽度)
# - 对于中文字体,汉字会被识别为宽字符并通过 wide_char_ratio 自动调整
# - 如需精细调整,可通过 --ratio 命令行参数覆盖
DEFAULT_VERTICAL_HORIZONTAL_RATIO = 2.0

# 最大差值和初始值 (用于字符匹配算法)
MAX_SUM_DATA = 1000000

# 像素最大值 (灰度图像素范围 0-255)
PIXEL_MAX_VALUE = 255.0

#endregion

#region 🟦 默认字符集

# 默认 ASCII 字符集 (包含基本 ASCII 字符及部分特殊符号)
DEFAULT_CHARSET = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

# 宽字符识别正则表达式模式
# 包含: 中文、日文、韩文、特殊符号、Emoji 等
import re
WIDE_CHAR_PATTERN = re.compile(r'[\u2010\u2012-\u2016\u2020-\u2022\u2025-\u2027\u2030\u2035\u203B\u203C\u2042\u2047-\u2049\u2051\u20DD\u20DE\u2100\u210A\u210F\u2121\u2135\u213B\u2160-\u216B\u2170-\u217B\u2215\u221F\u22DA\u22DB\u22EF\u2305-\u2307\u2312\u2318\u23B0\u23B1\u23BF-\u23CC\u23CE\u23DA\u23DB\u2423\u2460-\u24FF\u2600-\u2603\u2609\u260E\u260F\u2616\u2617\u261C-\u261F\u262F\u2668\u2672-\u267D\u26A0\u26BD\u26BE\u2702\u273D\u273F\u2740\u2756\u2776-\u277F\u2934\u2935\u29BF\u29FA\u29FB\u2B1A\u2E3A\u2E3B\u2E80-\u9FFF\uF900-\uFAFF\uFB00-\uFB04\uFE10-\uFE19\uFE30-\uFE6B\uFF01-\uFF60\uFFE0-\uFFE6\U0001F100-\U0001F10A\U0001F110-\U0001F12E\U0001F130-\U0001F16B\U0001F170-\U0001F19A\U0001F200-\U0001F251\U0002000B-\U0002F9F4]')

#endregion

#region 🟦 插值算法映射

# OpenCV 插值算法映射表
INTERPOLATION_MAP = {
    'nearest': 0,      # cv2.INTER_NEAREST
    'bilinear': 1,     # cv2.INTER_LINEAR
    'bicubic': 2,      # cv2.INTER_CUBIC
    'lanczos': 4       # cv2.INTER_LANCZOS4
}

# 默认插值算法
DEFAULT_INTERPOLATION = 'bilinear'

#endregion

#region 🟦 字体样式映射

# Windows 字体样式后缀映射 (针对常见字体)
FONT_STYLE_SUFFIX = {
    'regular': '',
    'bold': ',Bold',
    'italic': ',Italic',
    'bold-italic': ',Bold Italic'
}

# Windows 系统字体目录
WINDOWS_FONT_DIR = r'C:\Windows\Fonts'

#endregion

#region 🟦 日志配置

# 默认日志级别
DEFAULT_LOG_LEVEL = 'INFO'

#endregion
