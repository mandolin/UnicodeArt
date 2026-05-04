# 🟦 全局捕获指示。-1：使cprint不做任何输出；0：使cprint只在force_capture==1时执行输出（方便其它程序捕获最终结果）；1：使cprint始终都做输出；2：在调试时使用，根据调试标签对应输出。
global_capture = 0
# 🟦 全局调试标签集。cprint会根据global_capture和global_debug_tags的值决定是否输出。
global_debug_tags = []