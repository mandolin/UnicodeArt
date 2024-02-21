# UnicodeArt

本项目是基于[asciifier](https://github.com/yutotakano/asciifier)做了些调整和改进：优化了程序结构、优化了一些细节处理、增加了对宽字符的处理(基于特定混合等宽字体)。

主要功能为：根据输入的文本或图片生成相应的字符画。


## 使用方法

`python3 main.py [-h] [-c CONFIG] (-i IMAGE | -t TEXT) [-a CHARS] [-o OUTPUT] [-e HEIGHT] [-w WIDTH] [-f FONT] [-r RATIO] [-v] [-m MATRIX] [-p PRINT]`

```cmd
options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        配置文件路径
  -i IMAGE, --image IMAGE
                        任何cv2支持的图像文件
  -t TEXT, --text TEXT  一些文本字符串
  -a CHARS, --chars CHARS
                        用来构成字符画的基本字符
  -o OUTPUT, --output OUTPUT
                        生成文件的路径
  -e HEIGHT, --height HEIGHT
                        输出高度，即行数，也用作字体大小
  -w WIDTH, --width WIDTH
                        输出宽度，即字符画横向对应的字符数
  -f FONT, --font FONT  用于显示的文本字体
  -r RATIO, --ratio RATIO
                        每个字符相对于其宽度的高度倍数
  -v, --invert          反转图像
  -m MATRIX, --matrix MATRIX
                        用于采样的矩阵大小
  -p PRINT, --print PRINT
                        执行print(all:全部，为默认值；spec:指定，用于外部调用；no:不执行print输出)
```

## 示例

`python3 main.py -o output.txt -t "黑白あき123ABab" --font "C:\Windows\Fonts\SimSun.ttc" --height 20`
