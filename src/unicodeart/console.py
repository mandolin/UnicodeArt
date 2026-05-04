#!/usr/bin/env python3

import os
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
    #region 🟦㈠ 定义参数解析器对象p并初始化
    p=unicodeart_util.get_parser()
    #endregion

    #region 🟦㈡ 解析命令行参数

    """
    解析命令行参数并初始化相关变量
    包括图像路径、文本字符串、字符集、输出路径、尺寸参数等
    同时处理参数类型转换和全局变量设置
    """
    args = p.parse_args()
    #region 🔶① 定义一些后续将使用的参数变量并将args属性值赋给它们
    image_file_path           = args.image        # 图像文件路径
    text_string               = args.text         # 要转换的文本字符串
    chars                     = args.chars        # 使用的字符集
    output_path               = args.output       # 输出文件路径
    height                    = args.height       # 字符画图像高度
    width                     = args.width        # 字符画图像宽度
    art_font                  = args.font         # 字符画图像字体
    invert                    = args.invert       # 是否反转显示
    print_option              = args.print        # print选项设定
    debug_tags                = args.debug        # debug标签设定
    matrix_size               = int(args.matrix)  # 将字符串类型的矩阵大小参数转换为整数
    vertical_horizontal_ratio = float(args.ratio) # 将字符串类型的高度宽度比例参数转换为浮点数

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
        if not os.path.exists(image_file_path):
            cprint('err:图像未找到', 1)
            exit()
        
        # 使用cv2库读取图像（灰度图像）
        with open(image_file_path, 'rb') as f:
            image_file = cv2.imread(f.name, 0)
        # 如果图像未找到，打印错误消息并退出程序
        if image_file is None:
            cprint('err:无法读取图像', 1)
            exit()
    elif text_string is None:
        cprint('err:图像参数和文本参数不能都为空，请使用 --image 或者 --text', 1)
        exit()
    else:
        # 如果未指定图像文件路径但指定了文本参数，则还必须提供字体和高度参数
        if art_font is None:
            cprint('err:需要字体参数，请使用 --font', 1)
            exit()
        if height is None:
            cprint('err:需要高度参数，请使用 --height', 1)
            exit()

    #endregion

    #endregion

    #region 🟦㈢ 准备好操作台图像
    if image_file is not None:
        baseimg = image_file
    else:
        baseimg = unicodeart_util.get_baseimg(text_string, art_font, height, matrix_size)
    # 如果设置了反转选项，反转图像颜色（变为黑底效果）
    if invert is True:
        baseimg = cv2.bitwise_not(baseimg)
    #endregion

    cprint(baseimg)
    #region 🟦㈣ 根据操作台图像生成采样数组        
    sampling_array=unicodeart_util.get_sampling_array(baseimg, height, width, vertical_horizontal_ratio, matrix_size)
    #endregion

    #region 🟦㈤ 根据字符集参数准备好采样字符数组
    #todo3 暂用art_font用作字符字体，后期增加单独字符字体参数
    char_data, wide_char_data=unicodeart_util.get_char_data(chars, art_font, matrix_size, vertical_horizontal_ratio)
    #endregion
        
    #region 🟦㈥ 通过对采样字符数组和操作台图像采样数组进行比对，生成最终输出的字符串
    final_output = unicodeart_util.get_final_output(sampling_array, char_data, wide_char_data, output_path)
    cprint(final_output,1)
    #endregion


if __name__ == "__main__":
    cprint('console:__main__')
    console()     
    

    