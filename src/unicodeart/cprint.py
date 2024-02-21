from . import global_vars

def cprint(string, force_capture=0):    
    """
    打印字符串，如果全局变量global_capture为1，或全局变量global_capture为0且force_capture为1，则打印字符串。
    
    Args:
        string       : 要打印的字符串
        force_capture: 可选参数，默认值为0，表示是否强制捕获打印
    
    Returns:
        None
    """
    #print('cprint里的global_capture',global_vars.global_capture)

    if(global_vars.global_capture == 1 or (global_vars.global_capture == 0 and force_capture == 1)):
        print(string)