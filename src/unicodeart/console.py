#!/usr/bin/env python3

import os
import sys
import cv2
from . import unicodeart_util
from . import global_vars
from .cprint import cprint

def console():
    """
    控制台主函数，用于处理命令行参数并生成Unicode艺术图像
    
    该函数负责解析命令行参数，验证输入的有效性，读取或生成基础图像，
    然后根据指定的参数生成Unicode艺术图像输出。支持从图像文件或文本
    生成艺术图像，并提供多种自定义选项如字符集、尺寸、字体等。
    
    参数:
        通过命令行参数传入，包括:
        - image:  图像文件路径
        - text:   要转换的文本字符串
        - chars:  使用的字符集
        - output: 输出文件路径
        - height: 图像高度
        - width:  图像宽度
        - font:   字体参数
        - invert: 是否反转颜色
        - print:  打印选项
        - debug:  调试标签
        - matrix: 矩阵大小
        - ratio:  高度宽度比例
    
    返回值:
        无返回值，直接输出结果到控制台或文件
    """
    # 🟢 Windows 兼容性：设置标准输出为 UTF-8 编码
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except (AttributeError, IOError):
            # Python < 3.7 或重定向时可能失败
            pass
    
    #region 🟦㈠ 定义参数解析器对象p并初始化
    
    """
    两阶段参数解析策略：
    1. 第一阶段：仅解析 --lang 参数以确定语言环境
    2. 设置多语言支持
    3. 第二阶段：重新创建完整的解析器（此时帮助文本已翻译）
    """
    
    # 第一阶段：创建轻量级解析器仅获取 lang 参数
    import configargparse
    temp_parser = configargparse.ArgParser(add_help=False)
    temp_parser.add_argument('--lang', choices=['zh-CN', 'en-US'], default='zh-CN')
    temp_args, _ = temp_parser.parse_known_args()
    
    # 设置多语言支持
    from .i18n import set_language
    set_language(temp_args.lang)
    
    # 第二阶段：创建完整解析器（此时 _() 函数已切换到正确语言）
    p = unicodeart_util.get_parser()
    #endregion

    #region 🟦㈡ 解析命令行参数

    """
    解析命令行参数并初始化相关变量
    包括图像路径、文本字符串、字符集、输出路径、尺寸参数等
    同时处理参数类型转换和全局变量设置
    """
    args = p.parse_args()
    
    # 🟢 设置多语言支持
    from .i18n import set_language
    if hasattr(args, 'lang'):
        set_language(args.lang)
    
    #region 🔶① 定义一些后续将使用的参数变量并将args属性值赋给它们
    image_file_path           = args.image        # 图像文件路径
    text_string               = args.text         # 要转换的文本字符串
    chars                     = args.chars        # 使用的字符集
    output_path               = args.output       # 输出文件路径
    height                    = args.height       # 字符画图像高度
    width                     = args.width        # 字符画图像宽度
    art_font                  = args.font         # 字符画图像字体
    font_style                = args.font_style   # 字体样式 (regular/bold/italic/bold-italic)
    wide_char_ratio           = args.wide_char_ratio  # 宽字符匹配得分权重比例
    interpolation             = args.interpolation    # 图像 resize 插值算法
    invert                    = args.invert       # 是否反转显示
    print_option              = args.print        # print选项设定
    debug_tags                = args.debug        # debug标签设定
    matrix_size               = int(args.matrix)  # 将字符串类型的矩阵大小参数转换为整数
    vertical_horizontal_ratio = float(args.ratio) # 将字符串类型的高度宽度比例参数转换为浮点数
    
    # 🔶🟢 多行文本支持参数
    text_align                = args.text_align   # 文本对齐方式
    line_spacing              = args.line_spacing # 字符画行间距
    height_mode               = args.height_mode  # 高度模式 ('line' 或 'total')
    fontreduce                = args.font_reduce  # 字体大小缩减量

    #endregion

    #根据print_option设定global_vars.global_capture的值
    global_vars.global_capture = {
        'debug' : 2,
        'all'   : 1,
        'spec'  : 0
    }.get(print_option, -1)

    #根据debug_tags设定global_vars.global_debug_tags的值
    global_vars.global_debug_tags = debug_tags.split(',') if debug_tags else []

    cprint("----------测试调试标签：1,3,4", 2, "1,3,4")
    cprint("----------测试调试标签：2", 2, "2")
    cprint("----------测试调试标签：7,3,5", 2, "7,3,5")

    #region 🔶② 打印输出一些信息，供辅助说明及调试
    # 打印解析得到的参数
    cprint(args)
    cprint("----------")
    # 打印生成的帮助文档
    cprint(p.format_help())
    cprint("----------")
    # 打印参数及其值的格式化表示，这对于记录不同设置的来源很有用
    cprint(p.format_values())
    cprint("----------")
    #endregion

    #region 🔶③ 定义图像及相关错误处理
    image_file = None
    # 如果指定了图像文件路径
    if image_file_path is not None:
        # 首先判断图像路径是否有效
        from .i18n import _
        
        if not os.path.exists(image_file_path):
            cprint(_('error.file_not_found', path=image_file_path), 1)
            exit()
        
        # 使用cv2库读取图像（灰度图像）
        with open(image_file_path, 'rb') as f:
            image_file = cv2.imread(f.name, 0)
        # 如果图像未找到，打印错误消息并退出程序
        if image_file is None:
            cprint(_('error.cannot_read_image', path=image_file_path), 1)
            exit()
    elif text_string is None:
        cprint(_('error.missing_required_param', param_name='image or text'), 1)
        exit()
    else:
        # 如果未指定图像文件路径但指定了文本参数，则还必须提供字体和高度参数
        if art_font is None:
            cprint(_('error.missing_required_param', param_name='font'), 1)
            exit()
        if height is None:
            cprint(_('error.missing_required_param', param_name='height'), 1)
            exit()

    #endregion

    #endregion

    #region ㈢ 准备好操作台图像
    if image_file is not None:
        baseimg = image_file
    else:
        # 应用字体样式查找
        actual_font = unicodeart_util.load_font_with_style(art_font, font_style)
        baseimg = unicodeart_util.get_baseimg(text_string, actual_font, height, matrix_size, text_align, line_spacing, height_mode, fontreduce)
    # 如果设置了反转选项，反转图像颜色（变为黑底效果）
    if invert is True:
        baseimg = cv2.bitwise_not(baseimg)
    #endregion

    cprint(baseimg)
    
    # 🟢 根据高度模式计算实际采样高度
    if height_mode == 'total':
        # total 模式: height 就是总高度 (已包含行间距)
        actual_sampling_height = int(height)
    else:
        # line 模式 (默认): 计算总行数,然后当作 total 模式处理
        # 总行数 = 文本行高度 + 行间距高度
        lines_count = len(unicodeart_util.preprocess_text_input(text_string))
        text_lines_height = int(height) * lines_count
        spacing_lines_height = line_spacing * max(0, lines_count - 1)
        actual_sampling_height = text_lines_height + spacing_lines_height
    
    #region ㈣ 根据操作台图像生成采样数组        
    sampling_array = unicodeart_util.get_sampling_array(baseimg, actual_sampling_height, width, vertical_horizontal_ratio, matrix_size, interpolation)
    #endregion

    #region ㈤ 根据字符集参数准备好采样字符数组
    # note: art_font 同时用作渲染字体和显示字体，未来可增加单独字符字体参数
    actual_char_font = unicodeart_util.load_font_with_style(art_font, font_style)
    char_data, wide_char_data=unicodeart_util.get_char_data(chars, actual_char_font, matrix_size, vertical_horizontal_ratio, interpolation)
    #endregion
        
    #region ㈥ 通过对采样字符数组和操作台图像采样数组进行比对，生成最终输出的字符串
    final_output = unicodeart_util.get_final_output(sampling_array, char_data, wide_char_data, output_path, wide_char_ratio)
    cprint(final_output,1)
    #endregion