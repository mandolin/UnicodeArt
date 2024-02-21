import configargparse # 一个可使用配置文件的argparse替代库
import re
import math
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from .cprint import cprint

#region 获取参数解析器
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

    # 添加参数，用于指定字符、输出文件名等
    p.add_argument('-a', '--chars',  help='用来构成字符画的基本字符')
    p.add_argument('-o', '--output', help='生成文件的路径')
    p.add_argument('-e', '--height', help='输出高度，即行数，也用作字体大小')
    p.add_argument('-w', '--width',  help='输出宽度，即字符画横向对应的字符数')
    p.add_argument('-f', '--font',   help='用于显示的文本字体')
    # todo3 增加字符字体
    # todo3 增加“是否去除行尾空格”
    # todo3 增加图像resize操作时的插值设定参数
    p.add_argument('-r', '--ratio',  help='每个字符相对于其宽度的高度倍数', default='2.0')
    p.add_argument('-v', '--invert', help='反转图像', action='store_true')
    p.add_argument('-m', '--matrix', help='用于采样的矩阵大小', default='5')
    p.add_argument('-p', '--print',  help='执行print(all:全部，为默认值；spec:指定，用于外部调用；no:不执行print输出)', default='all')

    return p
#endregion

#region 操作台基准图像相关函数

# 生成操作台基准图像
def get_baseimg(text_string, art_font, height, matrix_size):
    """
    获取图像对象
    
    Args:
        text_string: 图像文件路径
        art_font   : 绘图所用字体
        height     : 图像高度
        matrix_size: 用于采样的矩阵大小

    
    Returns:
        Image: 图像对象
    """
    # 创建一个新的灰度图像
    '''
    'L' 表示图像的模式为灰度图像，后面的元组表示图像的尺寸（宽度、高度）
    rectunit为图格单元尺寸
    255 表示初始像素值，这里表示白色背景
    '''
    fontreduce=0 # todo 改为可配置项
    rectunit=int(height)*matrix_size

    # 从指定的字体文件中加载字体
    # afont 表示字体文件的路径
    # rectunit - fontreduce*2 表示字体的大小，减去 fontreduce*2 是为了避免字体过于接近图像边缘
    afont = ImageFont.truetype(art_font, rectunit - fontreduce*2)
    basewidth, text_widths=get_basewidth(fontreduce, text_string, afont, fontreduce*2)
    baseimg = Image.new('L', (basewidth, rectunit), 255)

    # 创建一个 ImageDraw 对象，用于在图像上绘制文本
    context = ImageDraw.Draw(baseimg)

    # 在图像上绘制文本
    # (fontreduce, fontreduce) 表示文本的起始位置坐标
    # 0 表示文本的颜色，这里表示黑色
    draw_text(text_widths, context, (fontreduce, fontreduce), text_string, afont, 0, fontreduce*2)

    # 将图像转换为NumPy数组
    baseimg = np.array(baseimg)

    return baseimg

# 获取操作台基准图像宽度
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
        # 添加间距
        basewidth += width+spacing
    return basewidth, text_widths

# 在操作台基准图像上绘制文本
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

#region 生成采样数组
def get_sampling_array(baseimg: np.ndarray, height, width, vertical_horizontal_ratio=2, matrix_size=5):
    """
    生成采样数组

    Args:
        baseimg (np.ndarray)                     : 输入图像
        height (int)                             : 输出图像的高度
        width (int)                              : 输出图像的宽度
        vertical_horizontal_ratio (int, optional): 水平和垂直比例，默认为2
        matrix_size (int, optional)              : 矩阵大小，默认为5

    Returns:
        np.ndarray: 采样数组
    """
    # 获取图像的高度和宽度
    source_height, source_width = baseimg.shape[:2]

    # 对于输出的每个字符/像素，从形状（rectsize_h，rectsize_w）计算密度
    # 这里的换算是因为通常的字体，包括控制台字体，高度大约是宽度的两倍（通过vertical_horizontal_ratio（args.ratio）配置）
    if height is not None and width is not None:
        # 如果指定了高度和宽度，则根据指定的高度和宽度计算矩形的大小
        rectsize_h = math.ceil(source_height / int(height))
        rectsize_w = math.ceil(source_width / (int(width) * vertical_horizontal_ratio))
    elif height is not None:
        # 如果只指定了高度，则根据指定的高度和纵横比例计算矩形的大小
        rectsize_h = math.ceil(source_height / int(height))
        rectsize_w = round(rectsize_h / vertical_horizontal_ratio)
    elif width is not None:
        # 如果只指定了宽度，则根据指定的宽度和纵横比例计算矩形的大小
        rectsize_w = math.ceil(source_width / (int(width) * vertical_horizontal_ratio))
        rectsize_h = round(rectsize_w * vertical_horizontal_ratio)
    else:
        # 如果既没有指定高度也没有指定宽度，则使用默认的矩形大小
        rectsize_h = 10
        rectsize_w = 5

    # 计算输出字符画的高度（行数）和宽度（每行字符数），以便容纳所有的矩形块
    output_height = math.ceil(source_height / rectsize_h)
    output_width  = math.ceil(source_width  / rectsize_w)

    # 初始化用于存储采样结果的数
    '''
    np.zeros: 这是 NumPy 库的函数，用于创建一个全零的数组。
    
    (output_height, output_width, matrix_size, matrix_size): 这个元组指定了数组的形状，即四个维度的大小。
    output_height: 输出图像的高度，表示在垂直方向上有多少个小矩形块。
    output_width: 输出图像的宽度，表示在水平方向上有多少个小矩形块。
    matrix_size: 每个小矩形块的高度。
    matrix_size: 每个小矩形块的宽度。
    这个数组 sampling_array 的形状实际上是一个四维数组。在上下文中，每个元素 sampling_array[i][j] 是一个 matrix_size x matrix_size 的矩阵，表示图像中对应位置的小矩形块的数据。

    这个数组将在后续的代码中用于存储图像的分割数据，每个小矩形块将被放置在相应的位置，用于后续的字符替代。
    '''
    sampling_array = np.zeros((output_height, output_width, matrix_size, matrix_size))

    # 循环遍历图像的行
    for y_index, actual_y_index in enumerate(range(0, len(baseimg), rectsize_h)):
        # 遍历源图像的垂直方向，每次移动 rectsize_h 个像素
        y = baseimg[actual_y_index]

        for x_index, actual_x_index in enumerate(range(0, len(y), rectsize_w)):
            # 遍历源图像的水平方向，每次移动 rectsize_w 个像素
            # 这里的每次循环对应于一个小矩形块或一个输出像素

            # 计算当前小矩形块的结束索引，避免超过图像边界
            blockend_y_index = min(actual_y_index + rectsize_h, len(baseimg) - 1)
            blockend_x_index = min(actual_x_index + rectsize_w, len(y) - 1)

            # 获取当前小矩形块的数据
            crop_region = baseimg[actual_y_index:blockend_y_index, actual_x_index:blockend_x_index]

            # 创建一个与矩形块相同大小的全白图像（值为255）
            padded_crop_region = np.ones((rectsize_h, rectsize_w)) * 255

            # 将矩形块的数据复制到全白图像中，实现裁剪
            padded_crop_region[:crop_region.shape[0], :crop_region.shape[1]] = crop_region

            # 调整裁剪后的矩形块大小为 matrix_size x matrix_size
            resized_padded_crop_region = cv2.resize(padded_crop_region, dsize=(matrix_size, matrix_size), interpolation=cv2.INTER_CUBIC)

            # 将调整大小后的矩形块数据存储在数组 sampling_array 的相应位置
            sampling_array[y_index][x_index] = resized_padded_crop_region
        
    # 将像素值缩放到 0-1 范围
    '''
    这是 NumPy 数组的一种矩阵计算。这行代码的目的是将数组 sampling_array 中的每个元素除以 255.0。这个操作实际上是对数组中的每个元素进行标准化，使它们的值在 0 到 1 之间。

    具体来说，假设 sampling_array 中的元素值为 0 到 255（通常表示灰度图像中的像素值），执行 sampling_array = sampling_array / 255.0 将每个元素的值除以 255.0，将它们转换为浮点数，并使它们的范围在 0 到 1 之间。

    这种标准化通常在深度学习等任务中很常见，因为它有助于模型更好地处理输入数据，并在训练过程中更好地收敛。标准化后的数据有助于消除不同特征之间的尺度差异，使模型更容易学习到有效的表示。
    '''
    sampling_array = sampling_array / 255.0

    return sampling_array
#endregion

#region 获取字符图像集
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
    - 对于东亚全角和半角字符，默认跳过不处理。若需支持双宽度字符，请在函数内添加相应的处理逻辑。
    - 字符集默认包含了基本的 ASCII 字符及部分特殊符号，如需使用自定义字符集，请提供有效的 `chars` 参数。

    Sample:
        ```python
            char_data = get_char_data('custom_charset.txt', 'arial.ttf', 64, 1.5)
        ```
    """
    charset = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]\\^_`abcdefghijklmnopqrstuvwxyz{|}~'
    charset1 = ' 这是一个测试'

    if chars is not None:
        charset = chars
        
    pattern        = re.compile('[\u2010\u2012-\u2016\u2020-\u2022\u2025-\u2027\u2030\u2035\u203B\u203C\u2042\u2047-\u2049\u2051\u20DD\u20DE\u2100\u210A\u210F\u2121\u2135\u213B\u2160-\u216B\u2170-\u217B\u2215\u221F\u22DA\u22DB\u22EF\u2305-\u2307\u2312\u2318\u23B0\u23B1\u23BF-\u23CC\u23CE\u23DA\u23DB\u2423\u2460-\u24FF\u2600-\u2603\u2609\u260E\u260F\u2616\u2617\u261C-\u261F\u262F\u2668\u2672-\u267D\u26A0\u26BD\u26BE\u2702\u273D\u273F\u2740\u2756\u2776-\u277F\u2934\u2935\u29BF\u29FA\u29FB\u2B1A\u2E3A\u2E3B\u2E80-\u9FFF\uF900-\uFAFF\uFB00-\uFB04\uFE10-\uFE19\uFE30-\uFE6B\uFF01-\uFF60\uFFE0-\uFFE6\U0001F100-\U0001F10A\U0001F110-\U0001F12E\U0001F130-\U0001F16B\U0001F170-\U0001F19A\U0001F200-\U0001F251\U0002000B-\U0002F9F4]')
    char_data      = []
    wide_char_data = []
    # 加载字体作为单元字符的基准字体
    font = ImageFont.truetype(char_font_file, matrix_size)
    # 用于绘制字符的图像单元
    letter_image = Image.new('L', (round(matrix_size / vertical_horizontal_ratio), matrix_size), 255)
    wide_letter_image = Image.new('L', (round(2*matrix_size / vertical_horizontal_ratio), matrix_size), 255)

    # 以下遍历每个字符，创建字符矩阵并追加到 `char_data`
    for char in charset:
        
        # 将字符及其对应矩阵添加到 `char_data`

        match_result = pattern.search(char)
        if match_result is not None:
            # 创建绘图对象
            canvas = ImageDraw.Draw(wide_letter_image)
            # 在图像上绘制字符
            canvas.text((0, 0), char, 0, font)
            # 添加到wide_char_data
            wide_char_data.append({
                'character': char,
                # 转换为 NumPy 数组，并将其调整大小为 (2*matrix_size, matrix_size)，这个数组即为当前字符对应的矩阵。/ 255.0 将矩阵中的像素值归一化到 [0, 1] 的范围。这是因为之前创建的灰度图像 letter_image 中的像素值范围是 [0, 255]。
                'matrix': cv2.resize(np.array(wide_letter_image), (2*matrix_size, matrix_size)) / 255.0
            })
            # 清空图像，准备绘制下一个字符
            canvas.rectangle((0, 0, round(2*matrix_size / vertical_horizontal_ratio), matrix_size), 255)

        else:
            # 创建绘图对象
            canvas = ImageDraw.Draw(letter_image)
            # 在图像上绘制字符
            canvas.text((0, 0), char, 0, font)
            # 添加到char_data
            char_data.append({
                'character': char,
                # 转换为 NumPy 数组，并将其调整大小为 (matrix_size, matrix_size)，这个数组即为当前字符对应的矩阵。/ 255.0 将矩阵中的像素值归一化到 [0, 1] 的范围。这是因为之前创建的灰度图像 letter_image 中的像素值范围是 [0, 255]。
                'matrix': cv2.resize(np.array(letter_image), (matrix_size, matrix_size)) / 255.0
            })
            # 清空图像，准备绘制下一个字符
            canvas.rectangle((0, 0, round(matrix_size / vertical_horizontal_ratio), matrix_size), 255)
        
        # 打印当前字符（可选，用于调试或查看字符处理的进展）
        cprint(char)
    
    #cprint(char_data,1)
    #cprint(wide_char_data,1)
    return char_data, wide_char_data
    
#endregion

#region 生成最终的输出字符串
def get_final_output(sampling_array, char_data, wide_char_data, output_path):
    """
    根据采样数组、字符数据、宽字符数据和输出路径生成最终输出结果。

    Args:
        sampling_array: 二维数组，表示采样矩阵
        char_data     : 字符数据列表，每个元素包含字符矩阵和字符文本表示
        wide_char_data: 宽字符数据列表，每个元素包含字符矩阵和字符文本表示
        output_path   : 输出路径，字符串类型

    Returns:
        final_output: 最终输出结果，字符串类型
    """
    final_output = ''
    skip_sign    = False
    # 遍历矩阵的每一行
    for index, row in enumerate(sampling_array):
        # 遍历矩阵的每个矩形
        for i, rectangle in enumerate(row):
            # 1. 对于每个字符，计算：矩形数据和字符数据的元素绝对差值之和
            # 2. 找到总和最小的字符的索引
            # 3. 输出该字符的文本表示
            # todo 增加其它匹配算法机制供可选（Mean Squared Error，MSE等）

            if skip_sign:
                skip_sign = False
                continue

            wide_sum_ratio = 2 # todo3 改为从配置获取
            sum_data       = [np.sum(np.absolute(rectangle - char['matrix'])) for char in char_data]
            sum_data_min   = 1000000
            if(len(char_data)>0):
                indice        = np.argmin(sum_data)
                sum_data_min  = sum_data[indice]
            if len(wide_char_data)>0 and i != len(row) - 1:
                sum_wide_data = [np.sum(np.absolute(np.hstack((rectangle, row[i+1])) - char['matrix'])) for char in wide_char_data]
                wide_indice   = np.argmin(sum_wide_data)
                if sum_wide_data[wide_indice] < wide_sum_ratio * sum_data_min:
                    #cprint(wide_char_data[0]['matrix'],1)
                    #cprint(row[52],1)
                    #cprint(i,1)
                    #cprint(np.absolute(np.hstack((row[52], row[i]))),1)
                    #exit()
                    skip_sign = True
                    final_output += f"{wide_char_data[wide_indice]['character']}"
                    continue
            
            final_output += f"{char_data[indice]['character']}"
            

        # 除非是最后一行，否则添加换行符
        if index != len(sampling_array) - 1:
            final_output = f"{final_output}\n"

    if output_path is not None and output_path != '':
        # 将生成的字符画输出到文件
        with open(output_path, "w", encoding="utf-8") as text_file:
            print(final_output, file=text_file)

    return final_output
#endregion

if __name__ == "__main__":
    exit()