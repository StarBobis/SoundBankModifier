# Wwise SoundBank Modifier

This tool is developed for modify or extract .bnk file.

You can run BNKModifierGUI.py to start.

You can learn some skill about Wwise Soundbank from test folder.

The test folder is generated during the testing process.

You can use foobar2000 and foo_input_vgmstream plugin located at Tools folder to easily test with wem file.

# Version
Python          3.9
PySimpleGUI         latest
SpeechRecognition   latest

# Environment 
pip install PySimpleGUI
pip install SpeechRecognition

# LICENSE 
This project use GNU GENERAL PUBLIC LICENSE.

# Todo list
    # Todo 指定codec进行转换（比较难还在摸索） 最后的难点
    # Todo 调用语音识别接口，自动识别每个语音文件的内容
    # Todo 展示wem文件的vorbis信息
    # Todo 读取本地csv表格文件来添加一列语音内容
    # Todo wem文件批量展示器
    # Todo 可以任意标记wem文件，记录到csv文件
    # TODO 一键提取永劫无间音频脚本
    # TODO 如何控制音量大小？默认替换完成后音量总是最大