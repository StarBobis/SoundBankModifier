"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from SoundBankUtil import *
import PySimpleGUI as sg
import os


def make_window():
    # 设置贴边
    sg.set_options(element_padding=(0, 0))

    # 顶部导航菜单
    menu_def = [['File', ['Open', 'Save As...']], ['Export All', ['Export .wem Format To...', 'Export .wav Format To...']]]
    # wem文件列表的右键菜单
    right_click_menu_def = ['', ['Play', 'Replace With .wem File', 'Replace With .wav File', 'Export to .wem File', 'Export to .wav File']]
    # wem文件列表
    table_def = [[]]

    # 创建layout
    layout = [
        [sg.Menu(menu_def, key='menu')],
        [sg.Table(table_def
                  , headings=["Id", "Offset", "Length (Bytes)", "Replacing with", "Content"]
                  , key="_table_"
                  , expand_x=True
                  , expand_y=True
                  , right_click_selects=True
                  , right_click_menu=right_click_menu_def)]
    ]

    # 创建窗口，黄金比例
    window = sg.Window("SoundBankModifier",
                       layout,
                       size=(1000, 675))

    return window


def main():
    # 注意，因为识别语音内容需要网络畅通，而且处理速度很慢，所以默认关闭，可以通过修改为True来开启
    flag_recongition = True

    bnk_info = None  # bnk文件信息
    relative_path = os.path.dirname(__file__)  # 项目运行路径
    cache_path = relative_path + "\\.cache"  # .cache路径
    wav_cache_path = cache_path + "\\wavCache"  # wavCache路径
    wem_cache_path = cache_path + "\\wemCache"  # wemCache路径
    tmp_cache_path = cache_path + "\\tmpCache"  # tmpCache路径
    # 判断如果缓存路径不存在，则创建缓存路径
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
        print("不存在临时缓存目录，进行创建")
    if not os.path.exists(wav_cache_path):
        os.mkdir(wav_cache_path)
        print("不存在wav临时缓存目录，进行创建")
    if not os.path.exists(wem_cache_path):
        os.mkdir(wem_cache_path)
        print("不存在wem临时缓存目录，进行创建")
    if not os.path.exists(tmp_cache_path):
        os.mkdir(tmp_cache_path)
        print("不存在tmp临时缓存目录，进行创建")

    testexe_file = relative_path + '\\vgmstream-win\\test.exe'  # vgmstream中的test.exe路径

    # 创建GUI界面
    window = make_window()

    # 事件处理
    while True:
        event, value = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == 'Open':
            # 获取bnk文件路径
            input_bnk_path = sg.popup_get_file('SoundBank file to open', no_window=True, file_types=(("Wwise SoundBank File", "*.bnk .bnk"), ))

            # 判断是否没打开任何文件
            if input_bnk_path.endswith(".bnk"):
                print("打开文件路径：" + input_bnk_path)
                bnk_name = input_bnk_path.split("/")[-1]
                # 更新标题
                sg.Window.set_title(window, "SoundBankModifier    Moding: " + bnk_name)

                # 读取BNK文件信息
                bnk_info = get_bnk_info(input_bnk_path)

                # 刷新本地缓存
                refresh_cache(bnk_info, testexe_file, wav_cache_path, wem_cache_path, tmp_cache_path)

                # 动态添加table列
                DIDX = bnk_info.DIDX_Section
                wem_infos = DIDX.WEMInfos
                wem_table = []
                i = 0
                for wem_info_id in wem_infos:
                    wem_info = wem_infos.get(wem_info_id)

                    wem_table.append([])
                    wem_table[i].append([str(wem_info.id)])
                    wem_table[i].append([str(wem_info.offset)])
                    wem_table[i].append([str(wem_info.length)])
                    wem_table[i].append([])
                    if flag_recongition:
                        wem_table[i].append([recognize_by_wem_id(wem_info.id)])

                    i = i+1

                window["_table_"].update(wem_table)
                window.refresh()
            else:
                print("未打开任何bnk文件")

        elif event == 'Save As...':
            output_bnk_path = sg.popup_get_file('SoundBank file to save', no_window=True,save_as=True,
                                               file_types=(("Wwise SoundBank File", "*.bnk .bnk"),))
            print(output_bnk_path)
            if output_bnk_path != "":
                if bnk_info is None:
                    sg.popup_error("请先打开一个bnk文件")
                else:
                    save_bnk(bnk_info, output_bnk_path)
                    sg.popup("导出成功！")
            else:
                print("空路径无法保存")

        elif event == 'Export .wem Format To...':
            output_wav_folder = sg.popup_get_folder("Which folder to save wem files", no_window=True)

            if output_wav_folder != "":
                if bnk_info is None:
                    if output_wav_folder != "":
                        sg.popup_error("请先打开一个bnk文件")
                else:
                    # 将缓存中的wav复制到目标目录
                    copyfiles(wem_cache_path, output_wav_folder)
                    sg.popup("导出成功！")
            else:
                print("未选择要导出到的文件夹")

        elif event == 'Export .wav Format To...':
            output_wav_folder = sg.popup_get_folder("Which folder to save wav files", no_window=True)

            if output_wav_folder != "":
                if bnk_info is None:
                    sg.popup_error("请先打开一个bnk文件")
                else:
                    # 将缓存中的wav复制到目标目录
                    copyfiles(wav_cache_path, output_wav_folder)
                    sg.popup("导出成功！")
            else:
                print("未选择要导出到的文件夹")

        elif event == 'Play':
            if bnk_info is None:
                sg.popup_error("请先打开一个bnk文件")
            else:
                row, col = window["_table_"].get_last_clicked_position()
                table_info = window["_table_"].get()
                print(table_info[row][0][0])
                subprocess.call(
                    "C:\Program Files\Windows Media Player\wmplayer.exe " + wav_cache_path + "\\" + table_info[row][0][
                        0] + ".wav")

        elif event == 'Replace With .wem File':
            replace_wem_path = sg.popup_get_file('wem file to replace', no_window=True,
                                               file_types=(("Wwise wem File", "*.wem .wem"),))

            if replace_wem_path != "":
                if bnk_info is None:
                    sg.popup_error("请先打开一个bnk文件")
                else:
                    replace_wem_name = replace_wem_path.split("/")[-1]
                    print(replace_wem_name)

                    row, col = window["_table_"].get_last_clicked_position()
                    table_info = window["_table_"].get()
                    print("获取到table_info: ")
                    print(table_info)
                    # 用指定的wem进行替换
                    bnk_info = replace_wem(bnk_info, replace_wem_path, int(row)+1)

                    # 替换后需要更新缓存文件中对应的wem文件和wav文件
                    # 拼接出要被替换的wem的所在路径
                    original_wem_id = table_info[row][0][0]
                    original_wem_file_path = wem_cache_path + "\\" + str(original_wem_id) + ".wem"
                    original_wav_file_path = wav_cache_path + "\\" + str(original_wem_id) + ".wav"
                    replace_single_cache_wem(replace_wem_path, original_wem_file_path, original_wav_file_path,testexe_file)


                    # 更新列表状态
                    # 更新用哪个进行的替换
                    table_info[row][3] = [replace_wem_name]
                    # 更新offset 和length
                    DIDX = bnk_info.DIDX_Section
                    i = 0
                    for wem_info_id in DIDX.WEMInfos:
                        wem_info = DIDX.WEMInfos.get(wem_info_id)
                        table_info[i][1] = wem_info.offset
                        table_info[i][2] = wem_info.length
                        i = i + 1
                    window["_table_"].update(table_info)
                    window.refresh()
                    sg.popup("替换成功")

        elif event == 'Replace With .wav File':
            replace_wav_path = sg.popup_get_file('wav file to replace', no_window=True,
                                                 file_types=(("wav File", "*.wav .wav"),))

            if replace_wav_path != "":
                if bnk_info is None:
                    sg.popup_error("请先打开一个bnk文件")
                else:
                    # 调用vgmstream，把wav文件转为wem文件
                    wav_name = replace_wav_path.split("/")[-1].split(".wav")[0]
                    tmp_wem_path = tmp_cache_path + '\\'+wav_name
                    convert_wav_to_wem(testexe_file, replace_wav_path, tmp_wem_path)

                    row, col = window["_table_"].get_last_clicked_position()
                    table_info = window["_table_"].get()
                    print("获取到table_info: ")
                    print(table_info)
                    # 用指定的wem进行替换
                    bnk_info = replace_wem(bnk_info, tmp_wem_path, int(row) + 1)

                    # 替换后需要更新缓存文件中对应的wem文件和wav文件
                    # 拼接出要被替换的wem的所在路径
                    original_wem_id = table_info[row][0][0]
                    original_wem_file_path = wem_cache_path + "\\" + str(original_wem_id) + ".wem"
                    original_wav_file_path = wav_cache_path + "\\" + str(original_wem_id) + ".wav"
                    replace_single_cache_wav(replace_wem_path, original_wav_file_path, original_wem_file_path,
                                             testexe_file)

                    # 更新列表状态
                    # 更新用哪个进行的替换
                    table_info[row][3] = [wav_name+".wav"]
                    # 更新offset 和length
                    DIDX = bnk_info.DIDX_Section
                    i = 0
                    for wem_info_id in DIDX.WEMInfos:
                        wem_info = DIDX.WEMInfos.get(wem_info_id)
                        table_info[i][1] = wem_info.offset
                        table_info[i][2] = wem_info.length
                        i = i + 1
                    window["_table_"].update(table_info)
                    window.refresh()
                    sg.popup("替换成功")

        elif event == 'Export to .wem File':
            output_wav_folder = sg.popup_get_folder("Which folder to save wem file", no_window=True)
            if output_wav_folder != "":
                if bnk_info is None:
                    if output_wav_folder != "":
                        sg.popup_error("请先打开一个bnk文件")
                else:
                    output_wav_folderPath = output_wav_folder + "/"
                    row, col = window["_table_"].get_last_clicked_position()
                    table_info = window["_table_"].get()
                    copy_wav_path = wem_cache_path+"\\" + table_info[row][0][0] + ".wem"
                    output_wav_path = output_wav_folderPath + table_info[row][0][0] + ".wem"
                    shutil.copy(copy_wav_path, output_wav_path)
                    sg.popup("导出成功！")
            else:
                print("未选择要导出到的文件夹")


        elif event == 'Export to .wav File':
            output_wav_folder = sg.popup_get_folder("Which folder to save wav file", no_window=True)
            if output_wav_folder != "":
                if bnk_info is None:
                    if output_wav_folder != "":
                        sg.popup_error("请先打开一个bnk文件")
                else:
                    output_wav_folderPath = output_wav_folder + "/"
                    row, col = window["_table_"].get_last_clicked_position()
                    table_info = window["_table_"].get()
                    copy_wav_path = wav_cache_path+"\\" + table_info[row][0][0] + ".wav"
                    output_wav_path = output_wav_folderPath + table_info[row][0][0] + ".wav"
                    shutil.copy(copy_wav_path, output_wav_path)
                    sg.popup("导出成功！")
            else:
                print("未选择要导出到的文件夹")



    # 关闭窗口前，清空.cache目录下所有文件
    # 删除临时文件夹下面的所有文件(只删除文件,不删除文件夹)
    del_file(wav_cache_path)
    del_file(wem_cache_path)
    del_file(tmp_cache_path)
    # 关闭窗口
    window.close()
    # 正常退出
    exit(0)


if __name__ == '__main__':
    main()


