import os
import cv2
import unicodeart
import global_vars
from cprint import cprint

if __name__ == "__main__":

    #region 定义参数解析器对象p并初始化
    p=unicodeart.get_parser()
    #endregion

    #region 解析命令行参数

    args = p.parse_args()
    # 定义一些后续将使用的参数变量并将args属性值赋给它们
    image_file_path           = args.image
    text_string               = args.text
    chars                     = args.chars
    output_path               = args.output
    height                    = args.height
    width                     = args.width
    art_font                  = args.font
    invert                    = args.invert
    print_option              = args.print
    matrix_size               = int(args.matrix)  # 将字符串类型的矩阵大小参数转换为整数
    vertical_horizontal_ratio = float(args.ratio) # 将字符串类型的高度宽度比例参数转换为浮点数

    #根据print_option设定global_vars.global_capture的值
    global_vars.global_capture = {
        'all' : 1,
        'spec': 0
    }.get(print_option, -1)



    # 打印解析得到的参数
    cprint(args)
    cprint("----------")
    # 打印生成的帮助文档
    cprint(p.format_help())
    cprint("----------")
    # 打印参数及其值的格式化表示，这对于记录不同设置的来源很有用
    cprint(p.format_values())
    cprint("----------")

    #region  定义图像及相关错误处理
    image_file = None
    # 如果指定了图像文件路径
    if image_file_path is not None:
        # 首先判断图像路径是否有效
        if not os.path.exists(image_file_path):
            cprint('图像未找到', 1)
            exit()
        
        # 使用cv2库读取图像（灰度图像）
        with open(image_file_path, 'rb') as f:
            image_file = cv2.imread(f.name, 0)
        # 如果图像未找到，打印错误消息并退出程序
        if image_file is None:
            cprint('无法读取图像', 1)
            exit()
    elif text_string is None:
        cprint('图像参数和文本参数不能都为空，请使用 --image 或者 --text', 1)
        exit()
    else:
        # 如果未指定图像文件路径但指定了文本参数，则还必须提供字体和高度参数
        if art_font is None:
            cprint('需要字体参数，请使用 --font', 1)
            exit()
        if height is None:
            cprint('需要高度参数，请使用 --height', 1)
            exit()

    #endregion

    #endregion

    #region 准备好操作台图像
    if image_file is not None:
        baseimg = image_file
    else:
        baseimg = unicodeart.get_baseimg(text_string, art_font, height, matrix_size)
    # 如果设置了反转选项，反转图像颜色（变为黑底效果）
    if invert is True:
        baseimg = cv2.bitwise_not(baseimg)
    #endregion

    #region 根据操作台图像生成采样数组        
    sampling_array=unicodeart.get_sampling_array(baseimg, height, width, vertical_horizontal_ratio, matrix_size)
    #endregion

    #region 根据字符集参数准备好字符数组
    #todo3 暂用art_font用作字符字体，后期增加单独字符字体参数
    char_data, wide_char_data=unicodeart.get_char_data(chars, art_font, matrix_size, vertical_horizontal_ratio)
    #endregion
        
    #region 生成最终输出的字符串
    final_output = unicodeart.get_final_output(sampling_array, char_data, wide_char_data, output_path)
    cprint(final_output,1)
    #endregion

    #python main.py -o output.txt -t "黑白あき123ABab" --font "C:\Windows\Fonts\SimSun.ttc" --height 20
        

    