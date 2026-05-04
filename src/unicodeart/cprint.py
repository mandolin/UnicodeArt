from . import global_vars

def cprint(string, force_capture=0, debug_tags=""):    
    """
    打印字符串，如果全局变量global_capture为1，或全局变量global_capture不为-1且force_capture为1，则打印字符串。
    
    Args:
        string       : 要打印的字符串
        force_capture: 可选参数。默认值为0,不强制捕获打印;1,强制捕获打印;2,表示在调试模式下强制捕获打印
        debug_tags   : 可选参数。默认值为""，表示不添加调试标签
    
    Returns:
        None
    """
    #print('cprint里的global_capture',global_vars.global_capture)

    # 🔶 如果全局变量global_capture为1，或全局变量global_capture不为-1且force_capture为1，则打印字符串
    if(global_vars.global_capture == 1 or (global_vars.global_capture != -1 and force_capture == 1)):
        print(string)
    # 🔶 反之，如果全局变量global_capture为2且force_capture为2，则根据debug_tags进行打印
    elif(global_vars.global_capture == 2 and force_capture == 2):
        #如果debug_tags为空或者debug_tags(逗号拆分后的数组)包含的标签只要有一个在全局变量global_debug_tags中，则打印字符串
        if(debug_tags == "" or any(tag in debug_tags.split(",") for tag in global_vars.global_debug_tags)):
            print(string)
        