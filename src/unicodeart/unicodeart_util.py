import configargparse # 一个可使用配置文件的argparse替代库
import os
import re
import math
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from .cprint import cprint
from .config import (
    DEFAULT_FONT_REDUCE,
    DEFAULT_WIDE_CHAR_RATIO,
    DEFAULT_MATRIX_SIZE,
    DEFAULT_VERTICAL_HORIZONTAL_RATIO,
    MAX_SUM_DATA,
    PIXEL_MAX_VALUE,
    DEFAULT_CHARSET,
    WIDE_CHAR_PATTERN,
    INTERPOLATION_MAP,
    DEFAULT_INTERPOLATION,
)

#todo1 更新python官方仓库版本

#region 🟦获取参数解析器
def get_parser():
    """
    创建参数解析器对象，设置默认配置文件路径
    
    Args:
        无
    
    Returns:
        configargparse.ArgParser: 参数解析器对象
    
    """
    # 创建参数解析器对象，设置默认配置文件路径
    p = configargparse.ArgParser(config_file_open_func=lambda filename: open(
                filename, "r+", encoding="utf-8"
            ), default_config_files=['config.txt', '/etc/app/conf.d/*.conf', '~/.my_settings'], description='根据输入的文本或图片生成相应的字符画')

    # 添加参数，用于指定配置文件路径 #todo2 增加多语言说明机制
    p.add('-c', '--config', is_config_file=True, help='配置文件路径')

    # 创建互斥组，确保只能选择一个输入方式
    input_group = p.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--image', help='任何cv2支持的图像文件')  # 这个选项可以在配置文件中设置，因为它以'--'开头
    input_group.add_argument('-t', '--text',  help='一些文本字符串')

    # 添加其它参数，用于指定字符、输出文件名等
    p.add_argument('-a', '--chars',  help='用来构成字符画的基本字符')
    p.add_argument('-o', '--output', help='生成文件的路径')
    p.add_argument('-e', '--height', help='输出高度 (含义取决于 --height-mode)')
    p.add_argument('-w', '--width',  help='输出宽度，即字符画横向对应的字符数')
    p.add_argument('-f', '--font',   help='用于显示的文本字体')
    
    # 🔶🟢 多行文本支持参数
    p.add_argument('--text-align', choices=['left', 'center', 'right'], default='left',
                   help='多行文本对齐方式 (默认: left)')
    p.add_argument('--line-spacing', type=int, default=0,
                   help='字符画行间距 (对应输入文本行的视觉块之间的空行数,单位:字符画行数)')
    
    # 🔶🟢 高度模式参数
    p.add_argument('--height-mode', choices=['line', 'total'], default='line',
                   help='高度模式: line=每行字符画高度(默认), total=整体字符画总高度')
    
    # todo3 增加字符字体
    # todo2 增加字体类型（粗体、斜体等）
    # todo3 增加"是否去除行尾空格"
    # todo3 增加图像resize操作时的插值设定参数
    # ✅ 已实现多行文本支持
    # todo3 增加裱框设置选项
    p.add_argument('-r', '--ratio',  help='每个字符相对于其宽度的高度倍数', default='2.0')
    p.add_argument('-v', '--invert', help='反转图像', action='store_true')
    p.add_argument('-m', '--matrix', help='用于采样的矩阵大小', default='5')
    p.add_argument('-p', '--print',  help='执行print(all:全部；spec:指定，用于外部调用，为默认值；no:不执行print输出)', default='spec')
    p.add_argument('-d', '--debug',  help='调试模式下的标签指定(逗号分隔的字符串默认为空)', default='')

    return p
#endregion

#region 🟦 文本预处理相关函数

# 🔶 预处理文本输入,支持多行和文件读取
def preprocess_text_input(text_string):
    """
    预处理文本输入,支持 \n 分隔的多行文本和 @filename.txt 语法
    
    Args:
        text_string: 原始文本字符串
    
    Returns:
        list[str]: 处理后的文本行列表
    
    Example:
        >>> preprocess_text_input("line1\nline2")
        ['line1', 'line2']
        >>> preprocess_text_input("@test.txt")  # 从文件读取
        ['content from file']
    """
    # 检查是否是文件引用语法 (@filename.txt)
    if text_string.startswith('@'):
        file_path = text_string[1:]  # 去掉 @ 符号
        
        # 验证文件是否存在
        if not os.path.exists(file_path):
            cprint(f'err:文件未找到: {file_path}', 1)
            exit()
        
        # 读取文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 按换行符分割,保留空行
            lines = content.split('\n')
            # 移除末尾的空行(如果文件以换行符结尾)
            if lines and lines[-1] == '':
                lines.pop()
            return lines
        except Exception as e:
            cprint(f'err:无法读取文件 {file_path}: {str(e)}', 1)
            exit()
    
    # 普通文本,按 \n 分割
    lines = text_string.split('\n')
    return lines

#endregion

#region 🟦 操作台基准图像相关函数

# 🔶 生成操作台基准图像 (支持多行文本和高度模式)
def get_baseimg(text_string, art_font, height, matrix_size, text_align='left', line_spacing=0, height_mode='line'):
    """
    获取图像对象 (支持多行文本和高度模式)
    
    Args:
        text_string : 要绘制的文本字符串 (可以是多行,用 \n 分隔,或 @filename.txt 语法)
        art_font    : 绘图所用字体
        height      : 输出高度 (含义取决于 height_mode)
        matrix_size : 用于采样的矩阵大小
        text_align  : 文本对齐方式 ('left', 'center', 'right')
        line_spacing: 字符画行间距 (对应输入文本行的视觉块之间的空行数,单位:字符画行数)
        height_mode : 高度模式 ('line'=每行高度, 'total'=整体总高度)
    
    Returns:
        Image: 图像对象
    """
    
    # 🟢 预处理文本输入,支持多行和文件读取
    lines = preprocess_text_input(text_string)
    num_lines = len(lines)
    
    # 🟢 绘字时边缘预留空白尺寸
    fontreduce = DEFAULT_FONT_REDUCE
    
    # 🟢 根据高度模式计算整体图像高度
    if height_mode == 'total':
        # total 模式: height 表示整体总高度
        total_height_pixels = int(height) * matrix_size
    else:
        # line 模式 (默认): height 表示每行高度
        # 关键修正: 先计算纯文本高度,再额外加上行间距高度
        text_height_pixels = int(height) * matrix_size * num_lines
        
        # 如果有行间距,额外增加总高度
        if line_spacing > 0 and num_lines > 1:
            spacing_pixels = line_spacing * matrix_size * (num_lines - 1)
            total_height_pixels = text_height_pixels + spacing_pixels
        else:
            total_height_pixels = text_height_pixels
    
    #  计算每行的实际高度 (line 模式下,每行高度固定为 height * matrix_size)
    if height_mode == 'line':
        # line 模式: 每行高度固定,不受行间距影响
        rectunit = int(height) * matrix_size
    else:
        # total 模式: 需要根据总高度和行数计算每行高度
        if line_spacing > 0 and num_lines > 1:
            # 总空行高度
            total_spacing_pixels = line_spacing * matrix_size * (num_lines - 1)
            # 实际用于绘制文本的高度
            drawing_height = total_height_pixels - total_spacing_pixels
            rectunit = drawing_height // num_lines if num_lines > 0 else total_height_pixels
        else:
            rectunit = total_height_pixels // num_lines if num_lines > 0 else total_height_pixels
    
    # 确保每行高度至少为 2px (避免除以零)
    rectunit = max(rectunit, 2)
    
    cprint(['height_mode:', height_mode])
    cprint(['num_lines:', num_lines])
    cprint(['total_height_pixels:', total_height_pixels])
    cprint(['rectunit (per line):', rectunit])
    cprint(['line_spacing:', line_spacing])
    
    # 🟢 从指定的字体文件中加载字体
    afont = ImageFont.truetype(art_font, rectunit - fontreduce*2)
    
    # 🟢 计算每行的宽度和字符宽度列表
    all_line_widths = []  # 存储每行的总宽度
    all_text_widths = []  # 存储每行的字符宽度列表
    
    for line in lines:
        basewidth, text_widths = get_basewidth(0, line, afont, fontreduce*2)
        all_line_widths.append(basewidth)
        all_text_widths.append(text_widths)
    
    # 🟢 计算最终图像的宽度
    max_width = max(all_line_widths) if all_line_widths else rectunit
    
    # 🟢 创建一个新的灰度图像 (使用计算的总高度)
    baseimg = Image.new('L', (max_width, total_height_pixels), 255)
    
    # 🟢 创建一个 ImageDraw 对象，用于在图像上绘制文本
    context = ImageDraw.Draw(baseimg)
    
    # 🟢 逐行绘制文本,应用对齐方式
    current_y = fontreduce  # 当前行的 Y 坐标
    
    for i, line in enumerate(lines):
        line_width = all_line_widths[i]
        text_widths = all_text_widths[i]
        
        # 计算 X 坐标 (根据对齐方式)
        if text_align == 'left':
            x_offset = fontreduce
        elif text_align == 'center':
            x_offset = fontreduce + (max_width - line_width) // 2
        elif text_align == 'right':
            x_offset = fontreduce + (max_width - line_width)
        
        # 绘制该行文本
        draw_text(text_widths, context, (x_offset, current_y), line, afont, 0, fontreduce*2)
        
        # 更新 Y 坐标到下一行 (加上行间距)
        if i < num_lines - 1:
            # 如果不是最后一行,加上行间距 (line_spacing 个字符画行的高度)
            current_y += rectunit + (line_spacing * matrix_size)
        else:
            # 最后一行不需要加行间距
            current_y += rectunit
    
    cprint(['lines count:', num_lines])
    cprint(['all_line_widths:', all_line_widths])
    cprint(['max_width:', max_width])
    cprint(['final total_height:', total_height_pixels])
    
    # 🟢 将图像转换为NumPy数组
    #baseimg.save('v1.png')
    baseimg = np.array(baseimg)
    
    return baseimg

# 🔶 获取操作台基准图像宽度
def get_basewidth(position, text, font, spacing):
    """
    根据给定的字体和间距计算文本的基线宽度。
    
    Args:
        position (int): 文本的起始位置
        text (str)    : 要计算宽度的文本
        font (Font)   : 字体对象
        spacing (int) : 字符之间的间距
    
    Returns：
        basewidth (int)   : 文本的基线宽度
        text_widths (list): 每个字符的实际宽度列表
    """
    text_widths=[]
    basewidth=position
    for i, char in enumerate(text):
        # 获取字符实际宽度
        l,b, width, height=font.getbbox(text=char)
        text_widths.append(width)
        # 添加间距持续获取文本基线宽度
        basewidth += width+spacing
    return basewidth, text_widths

# 🔶 在操作台基准图像上绘制文本
def draw_text(text_widths, draw, position, text, font, fill, spacing):
    """
    绘制文本

    Args:
        text_widths (list)  : 每个字符的宽度列表
        draw        (object): 绘制对象
        position    (tuple) : 绘制位置
        text        (str)   : 要绘制的文本
        font        (object): 字体对象
        fill        (str)   : 填充颜色
        spacing     (int)   : 字间距

    Returns:
        None
    """
    x, y = position
    for i, char in enumerate(text):
        draw.text((x, y), char, fill=fill, font=font)
        # 添加间距
        x += text_widths[i]+spacing
#endregion

#region 🟦 采样数组生成辅助函数

# 🔶 计算采样块尺寸
def _calculate_block_size(
    source_height: int,
    source_width: int,
    output_height: int,
    output_width: int,
    vertical_horizontal_ratio: float
) -> tuple:
    """
    根据源图像尺寸和输出尺寸计算采样块大小
    
    Args:
        source_height: 源图像高度
        source_width: 源图像宽度
        output_height: 输出行数 (可能为 None)
        output_width: 输出列数 (可能为 None)
        vertical_horizontal_ratio: 垂直水平比例
    
    Returns:
        tuple: (rectsize_h, rectsize_w) 采样块的高度和宽度
    
    Note:
        - 确保返回值 >= 1,避免除以零错误
        - 当源图像尺寸小于输出尺寸时,会自动调整块尺寸为最小值 1
    """
    if output_height is not None and output_width is not None:
        # 如果指定了高度和宽度，则根据指定的高度和宽度计算矩形的大小
        rectsize_h = math.ceil(source_height / int(output_height))
        rectsize_w = math.ceil(source_width / (int(output_width) * vertical_horizontal_ratio))
    elif output_height is not None:
        # 如果只指定了高度，则根据指定的高度和纵横比例计算矩形的大小
        rectsize_h = math.ceil(source_height / int(output_height))
        rectsize_w = round(rectsize_h / vertical_horizontal_ratio)
    elif output_width is not None:
        # 如果只指定了宽度，则根据指定的宽度和纵横比例计算矩形的大小
        rectsize_w = math.ceil(source_width / (int(output_width) * vertical_horizontal_ratio))
        rectsize_h = round(rectsize_w * vertical_horizontal_ratio)
    else:
        # 如果既没有指定高度也没有指定宽度，则使用默认的矩形大小
        rectsize_h = DEFAULT_MATRIX_SIZE * 2  # 保持一定的默认比例，或者使用之前的 10
        rectsize_w = DEFAULT_MATRIX_SIZE      # 保持一定的默认比例，或者使用之前的 5
    
    # 🟢 确保块尺寸不为零,同时保持垂直水平比例
    # rectsize_h 至少为 2,保证有足够的采样精度
    # rectsize_w 至少为 1,避免除以零错误
    rectsize_h = max(2, rectsize_h)
    rectsize_w = max(1, rectsize_w)
        
    return rectsize_h, rectsize_w

# 🔶 计算输出维度
def _calculate_output_dimensions(
    source_height: int,
    source_width: int,
    block_h: int,
    block_w: int
) -> tuple:
    """
    计算输出字符画的行数和列数
    
    Args:
        source_height: 源图像高度
        source_width: 源图像宽度
        block_h: 采样块高度
        block_w: 采样块宽度
    
    Returns:
        tuple: (output_height, output_width) 输出的行数和列数
    """
    output_height = math.ceil(source_height / block_h)
    output_width = math.ceil(source_width / block_w)
    return output_height, output_width

# 🔶 提取并采样单个图像块
def _extract_and_sample_block(
    baseimg: np.ndarray,
    start_y: int,
    start_x: int,
    block_h: int,
    block_w: int,
    matrix_size: int
) -> np.ndarray:
    """
    从源图像中提取一个块并进行缩放采样
    
    Args:
        baseimg: 源图像数组
        start_y: 起始Y坐标
        start_x: 起始X坐标
        block_h: 块高度
        block_w: 块宽度
        matrix_size: 目标矩阵尺寸
    
    Returns:
        np.ndarray: 缩放后的归一化矩阵 (matrix_size x matrix_size)
    """
    # 计算结束索引，避免超过图像边界
    end_y = min(start_y + block_h, baseimg.shape[0])
    end_x = min(start_x + block_w, baseimg.shape[1])
    
    # 获取当前小矩形块的数据
    crop_region = baseimg[start_y:end_y, start_x:end_x]
    
    # 创建一个与矩形块相同大小的全白图像（值为255）
    padded_crop = np.ones((block_h, block_w)) * PIXEL_MAX_VALUE
    
    # 将矩形块的数据复制到全白图像中，实现裁剪填充
    padded_crop[:crop_region.shape[0], :crop_region.shape[1]] = crop_region
    
    # 调整裁剪后的矩形块大小为 matrix_size x matrix_size
    resized = cv2.resize(padded_crop, dsize=(matrix_size, matrix_size), interpolation=cv2.INTER_CUBIC)
    
    return resized

#endregion

#region 🟦 生成采样数组
def get_sampling_array(baseimg: np.ndarray, height, width, vertical_horizontal_ratio=DEFAULT_VERTICAL_HORIZONTAL_RATIO, matrix_size=DEFAULT_MATRIX_SIZE):
    """
    生成采样数组

    Args:
        baseimg (np.ndarray)                     : 输入图像
        height (int)                             : 输出字符画图像的高度
        width (int)                              : 输出字符画图像的宽度
        vertical_horizontal_ratio (int, optional): 水平和垂直比例，默认为2
        matrix_size (int, optional)              : 矩阵大小，默认为5

    Returns:
        np.ndarray: 采样数组
    """
    cprint(['get_sampling_array',height, width, vertical_horizontal_ratio, matrix_size])
    
    # 🔶 获取图像的高度和宽度
    source_height, source_width = baseimg.shape[:2]
    cprint(['source_height,source_width',source_height,source_width])

    # 🔶 计算采样块尺寸
    rectsize_h, rectsize_w = _calculate_block_size(
        source_height, source_width, height, width, vertical_horizontal_ratio
    )
    
    #  计算输出维度
    output_height, output_width = _calculate_output_dimensions(
        source_height, source_width, rectsize_h, rectsize_w
    )

    # 🔶 初始化用于存储采样结果的数组
    sampling_array = np.zeros((output_height, output_width, matrix_size, matrix_size))

    # 🔶 循环遍历图像的行和列，提取并采样每个块
    for y_index, actual_y in enumerate(range(0, len(baseimg), rectsize_h)):
        for x_index, actual_x in enumerate(range(0, len(baseimg[0]), rectsize_w)):
            # 提取并采样单个图像块
            block = _extract_and_sample_block(
                baseimg, actual_y, actual_x, 
                rectsize_h, rectsize_w, matrix_size
            )
            
            # 存储到采样数组
            sampling_array[y_index][x_index] = block
        
    # 🔶 将像素值缩放到 0-1 范围
    sampling_array = sampling_array / PIXEL_MAX_VALUE

    return sampling_array
#endregion

#region 🟦 字符处理辅助函数

# 🔶 判断字符是否为宽字符
def _is_wide_character(char: str, pattern: re.Pattern) -> bool:
    """
    判断给定字符是否为宽字符
    
    Args:
        char: 待判断的字符
        pattern: 宽字符匹配的正则表达式模式
    
    Returns:
        bool: 如果是宽字符返回 True,否则返回 False
    """
    return pattern.search(char) is not None

# 🔶 创建字符画布
def _create_character_canvas(
    matrix_size: int,
    vertical_horizontal_ratio: float,
    is_wide: bool = False
) -> Image.Image:
    """
    创建用于绘制字符的画布
    
    Args:
        matrix_size: 矩阵尺寸
        vertical_horizontal_ratio: 垂直水平比例
        is_wide: 是否为宽字符画布
    
    Returns:
        Image: 新建的灰度图像画布
    """
    if is_wide:
        width = round(2 * matrix_size / vertical_horizontal_ratio)
    else:
        width = round(matrix_size / vertical_horizontal_ratio)
    
    return Image.new('L', (width, matrix_size), 255)

# 🔶 渲染字符到矩阵
def _render_char_to_matrix(
    char: str,
    canvas: Image.Image,
    font: ImageFont.FreeTypeFont,
    matrix_size: int,
    is_wide: bool = False,
    vertical_horizontal_ratio: float = DEFAULT_VERTICAL_HORIZONTAL_RATIO
) -> np.ndarray:
    """
    将字符渲染到画布并转换为归一化矩阵
    
    Args:
        char: 要渲染的字符
        canvas: 绘图画布
        font: 字体对象
        matrix_size: 目标矩阵尺寸
        is_wide: 是否为宽字符
        vertical_horizontal_ratio: 垂直水平比例
    
    Returns:
        np.ndarray: 归一化到 [0, 1] 的灰度矩阵
    """
    # 创建绘图对象
    draw = ImageDraw.Draw(canvas)
    
    # 绘制字符
    draw.text((0, 0), char, 0, font)
    
    # 计算目标尺寸
    if is_wide:
        target_size = (2 * matrix_size, matrix_size)
        canvas_width = round(2 * matrix_size / vertical_horizontal_ratio)
    else:
        target_size = (matrix_size, matrix_size)
        canvas_width = round(matrix_size / vertical_horizontal_ratio)
    
    # 转换为数组并缩放
    matrix = cv2.resize(np.array(canvas), target_size) / PIXEL_MAX_VALUE
    
    # 清空画布
    draw.rectangle((0, 0, canvas_width, matrix_size), 255)
    
    return matrix

#endregion

#region 🟦 获取字符图像集
def get_char_data(chars, char_font_file, matrix_size, vertical_horizontal_ratio):
    """
    从指定字符集中为每个字符生成对应的灰度图像矩阵，并将数据结构化后返回。

    Args:
        chars (str, optional)            : 字符集，如果提供则会覆盖默认的 ASCII 字符集。内容应包含待处理的一系列字符，支持多语言字符。
        char_font_file (str)             : 字体文件路径，用于绘制字符图像。
        matrix_size (int)                : 单个字符图像的高度，同时也是归一化后的宽度（对于非宽字符）。
        vertical_horizontal_ratio (float): 字符图像画布宽度与高度的比例。

    Returns:
        list[dict]: 包含字符信息及其对应图像矩阵的字典列表，每个字典结构如下：
            {
                'character': str,  # 当前字符
                'matrix': np.ndarray,  # 归一化到 [0, 1] 范围内的灰度图像矩阵，尺寸为 (matrix_size, matrix_size)
            }

    Note:
    - 对于东亚全角和半角字符，已增加单独处理，但须使用对应可用的字体。
    - 字符集默认包含了基本的 ASCII 字符及部分特殊符号，如需使用自定义字符集，请提供有效的 `chars` 参数。

    Sample:
        ```python
            char_data = get_char_data('custom_charset.txt', 'arial.ttf', 64, 1.5)
        ```
    """

    #region 🔶 准备好相关变量
    # 🟢 使用默认字符集或用户提供的字符集
    charset = DEFAULT_CHARSET if chars is None else chars
        
    # 🟢 编译宽字符匹配模式
    pattern = re.compile(WIDE_CHAR_PATTERN)
    
    # 🟢 字符矩阵数据
    char_data      = []
    # 🟢 宽字符矩阵数据
    wide_char_data = []
    
    # 🟢 加载字体作为单元字符的基准字体
    font = ImageFont.truetype(char_font_file, matrix_size)
    #endregion

    #region 🔶 遍历每个字符，创建字符矩阵并追加到 `char_data` 和 `wide_char_data`

    for char in charset:
        
        # 🟢 判断是否为宽字符
        if _is_wide_character(char, pattern):
            # 🔹 创建宽字符画布
            canvas = _create_character_canvas(matrix_size, vertical_horizontal_ratio, is_wide=True)
            
            # 🔹 渲染字符到矩阵
            matrix = _render_char_to_matrix(
                char, canvas, font, matrix_size, 
                is_wide=True, 
                vertical_horizontal_ratio=vertical_horizontal_ratio
            )
            
            # 🔹 添加到 wide_char_data
            wide_char_data.append({
                'character': char,
                'matrix': matrix
            })

        # 🟢 普通Ascii字符
        else:
            # 🔹 创建普通字符画布
            canvas = _create_character_canvas(matrix_size, vertical_horizontal_ratio, is_wide=False)
            
            # 🔹 渲染字符到矩阵
            matrix = _render_char_to_matrix(
                char, canvas, font, matrix_size,
                is_wide=False,
                vertical_horizontal_ratio=vertical_horizontal_ratio
            )
            
            # 🔹 添加到 char_data
            char_data.append({
                'character': char,
                'matrix': matrix
            })
        
        # 打印当前字符（可选，用于调试或查看字符处理的进展）
        cprint(char)
    #endregion
    
    #cprint(char_data,1)
    #cprint(wide_char_data,1)

    return char_data, wide_char_data
#endregion

#region 🟦 字符匹配辅助函数

# 🔶 计算匹配得分
def _calculate_match_score(rectangle: np.ndarray, char_matrix: np.ndarray) -> float:
    """
    计算矩形数据与字符矩阵的匹配得分 (绝对差值之和)
    
    Args:
        rectangle: 采样矩形数据
        char_matrix: 字符矩阵数据
    
    Returns:
        float: 匹配得分 (越小越匹配)
    """
    return np.sum(np.absolute(rectangle - char_matrix))

# 🔶 查找最佳普通字符
def _find_best_normal_char(
    rectangle: np.ndarray,
    char_data: list
) -> tuple:
    """
    在普通字符集中找到最佳匹配字符
    
    Args:
        rectangle: 采样矩形数据
        char_data: 普通字符数据列表
    
    Returns:
        tuple: (indice, min_score) 最佳字符索引和最小得分
               如果 char_data 为空,返回 (None, MAX_SUM_DATA)
    """
    if len(char_data) == 0:
        return None, MAX_SUM_DATA
    
    # 计算每个字符的匹配得分
    sum_data = [_calculate_match_score(rectangle, char['matrix']) for char in char_data]
    
    # 找到最小得分的索引
    indice = np.argmin(sum_data)
    min_score = sum_data[indice]
    
    return indice, min_score

# 🔶 查找最佳宽字符
def _find_best_wide_char(
    rectangle: np.ndarray,
    next_rectangle: np.ndarray,
    wide_char_data: list
) -> tuple:
    """
    在宽字符集中找到最佳匹配字符 (合并两个相邻矩形)
    
    Args:
        rectangle: 当前采样矩形
        next_rectangle: 下一个采样矩形
        wide_char_data: 宽字符数据列表
    
    Returns:
        tuple: (wide_indice, wide_score) 最佳宽字符索引和得分
    """
    # 合并两个相邻矩形
    combined = np.hstack((rectangle, next_rectangle))
    
    # 计算每个宽字符的匹配得分
    sum_wide_data = [_calculate_match_score(combined, char['matrix']) for char in wide_char_data]
    
    # 找到最小得分的索引
    wide_indice = np.argmin(sum_wide_data)
    wide_score = sum_wide_data[wide_indice]
    
    return wide_indice, wide_score

# 🔶 决定使用普通字符还是宽字符
def _decide_character_type(
    normal_score: float,
    wide_score: float,
    wide_ratio: float,
    is_last_in_row: bool
) -> str:
    """
    根据得分决定使用普通字符还是宽字符
    
    Args:
        normal_score: 普通字符最小得分
        wide_score: 宽字符最小得分
        wide_ratio: 宽字符权重比例
        is_last_in_row: 是否为行末尾
    
    Returns:
        str: 'normal' 或 'wide'
    """
    # 如果是行末尾,不能使用宽字符
    if is_last_in_row:
        return 'normal'
    
    # 如果宽字符得分足够小,则使用宽字符
    if wide_score < wide_ratio * normal_score:
        return 'wide'
    
    return 'normal'

#endregion

#region 🟦 生成最终的输出字符串
def get_final_output(sampling_array, char_data, wide_char_data, output_path, wide_sum_ratio=DEFAULT_WIDE_CHAR_RATIO):
    """
    根据采样数组、字符数据、宽字符数据和输出路径生成最终输出结果。

    Args:
        sampling_array : 二维数组，表示采样矩阵
        char_data      : 字符数据列表，每个元素包含字符矩阵和字符文本表示
        wide_char_data : 宽字符数据列表，每个元素包含字符矩阵和字符文本表示
        output_path    : 输出路径，字符串类型
        wide_sum_ratio : 宽字符匹配得分的权重比例

    Returns:
        final_output: 最终输出结果，字符串类型
    """
    final_output = ''
    # 跳过标识，用于宽字符匹配时跳过下一个矩形
    skip_sign = False
    
    # 🔶 遍历矩阵的每一行
    for index, row in enumerate(sampling_array):
        # 🟢 遍历矩阵的每个矩形
        for i, rectangle in enumerate(row):
            # 🔹 如果跳过标识为真(说明上一次用的宽字符)，则跳过当前矩形
            if skip_sign:
                skip_sign = False
                continue

            # 🟢 查找最佳普通字符
            normal_indice, normal_score = _find_best_normal_char(rectangle, char_data)

            # 🟢 查找最佳宽字符 (如果不是行末尾且有宽字符集)
            is_last_in_row = (i == len(row) - 1)
            use_wide = False
            wide_indice = None
            
            if len(wide_char_data) > 0 and not is_last_in_row:
                wide_indice, wide_score = _find_best_wide_char(
                    rectangle, row[i + 1], wide_char_data
                )
                
                # 决定使用哪种字符
                char_type = _decide_character_type(
                    normal_score, wide_score, wide_sum_ratio, is_last_in_row
                )
                
                if char_type == 'wide':
                    use_wide = True
            
            # 🟢 根据决定添加字符
            if use_wide and wide_indice is not None:
                skip_sign = True
                final_output += wide_char_data[wide_indice]['character']
            elif normal_indice is not None:
                final_output += char_data[normal_indice]['character']
            else:
                # 如果两者都为空,使用占位符
                final_output += '?'
            
        # 🟢 除非是最后一行，否则添加换行符
        if index != len(sampling_array) - 1:
            final_output = f"{final_output}\n"
    
    # 🔶 如果output_path不为空且不是空字符串，则输出到文件
    if output_path is not None and output_path != '':
        # 将生成的字符画输出到文件
        with open(output_path, "w", encoding="utf-8") as text_file:
            print(final_output, file=text_file)

    return final_output
#endregion

if __name__ == "__main__":
    exit()