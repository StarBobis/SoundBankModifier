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

import os
# Test02 学习一下前辈的思路，先把所有东西，DIDX所有部分都准备好
# 先读取，再写出


class BNKFileInfo:
    BKHD_Section = None
    DIDX_Section = None
    DATA_Section = None
    REST_Section = None  # 除了BKHD，DIDX，DATA部分外，剩余的字节
    pass


class BKHDSection:
    bkhd_bytes = None  # BKHD部分所有字节

    bkhd_name = None
    bkhd_length = None
    bkhd_version = None
    bkhd_soundBankId = None
    bkhd_alwaysZero1 = None
    bkhd_alwaysZero2 = None
    '''
    The BKHD section (Bank Header) contains the version number and the SoundBank id.
    ● bkhd_name             42 4B 48 44 -- BKHD
    ● bkhd_length           uint32: length of section
    ● bkhd_version          uint32: version number of this SoundBank
    ● bkhd_soundBankId      uint32: id of this SoundBank
    ● bkhd_alwaysZero1      uint32: always zero
    ● bkhd_alwaysZero2      uint32: always zero
    '''


class DIDXSection:
    didx_bytes = None  # DIDX部分所有字节，注意如果发生了wem文件替换需要重新赋值

    didx_name = None
    didx_length = None
    WEMInfos = None

    '''
    The DIDX (Data Index) section contains the references to the .wem files embedded in the SoundBank. 
    Each sound file is described with 12 bytes, 
    so you can get the number of embedded files by dividing the section length by 12.
    ● didx_name         44 49 44 58 -- DIDX
    ● didx_length       uint32: length of section
    ● FOR EACH (embedded .wem file) {
      ○ uint32: .wem file id
      ○ uint32: offset from start of DATA section
      ○ uint32: length in bytes of .wem file
    ● } END FOR
    '''


class WEMInfo:
    wem_bytes = None
    id = None
    offset = None
    length = None


class DATASection:
    data_bytes = None

    data_name = None
    data_length = None
    '''
    The DATA section contains the .wem files, not encoded, and immediately following each other. 
    It is not recommended to read this section by itself but instead to immediately jump to 
    the correct position based on the offset given in the DIDX or HIRC section.
    ● data_name         44 41 54 41 -- DATA
    ● data_length       uint32: length of section
    ● FOR EACH (embedded .wem file) {
        ○ byte[]: the .wem file with the length as given in the DIDX section, and starting with 52 49 46 46 -- RIFF.
    ● } END FOR
    '''


class RESTSection:
    rest_bytes = None

    '''
    ENVS section (The ENVS section (Environments?) section is yet to be analysed.)
    FXPR section (The FXPR section (Effects production?) section is yet to be analysed.)
    HIRC section 
    '''


# 类定义好之后，开始读取所有信息到BNKFileInfo类
input_bnk_path = "C:/Users/user/Desktop/dialogue_outgame_tarka.bnk"
input_file = open(input_bnk_path,"rb")
print("开始读取文件，当前指针位置："+str(input_file.tell()))
input_bnk_size = os.path.getsize(input_bnk_path)

bnkFileInfo = BNKFileInfo()
BKHD = BKHDSection()
DIDX = DIDXSection()
DATA = DATASection()
REST = RESTSection()

# 1.读取BKHD部分
bkhd_StartPosition = 0
BKHD.bkhd_name = input_file.read(4)
BKHD.bkhd_length = int.from_bytes(input_file.read(4), "little")
# 读取BKHD bytes，读取后进入DIDX部分
input_file.seek(bkhd_StartPosition)
BKHD.bkhd_bytes = input_file.read(BKHD.bkhd_length + 4 + 4)


# 2.读取DIDX部分
didx_StartPosition = input_file.tell()
DIDX.didx_name = input_file.read(4)
DIDX.didx_length = int.from_bytes(input_file.read(4), "little")
# 读取DIDX bytes，读取后进入DATA部分
input_file.seek(didx_StartPosition)
DIDX.didx_bytes = input_file.read(DIDX.didx_length + 4 + 4)

# 3.读取DATA部分
data_StartPosition = input_file.tell()
DATA.data_name = input_file.read(4)
DATA.data_length = int.from_bytes(input_file.read(4),"little")
# 读取DATA bytes，读取后进入REST部分
input_file.seek(data_StartPosition)
DATA.data_bytes = input_file.read(DATA.data_length + 4 + 4)

# 4.读取REST部分
rest_length = input_bnk_size - input_file.tell()
REST.rest_bytes = input_file.read(rest_length)

# 5.读取WEMInfo列表
didx_TruePosition = didx_StartPosition + 4 + 4
data_TruePosition = data_StartPosition + 4 + 4

# (1)跳转到DIDX存储WEM信息的部分
input_file.seek(didx_TruePosition)

# (2)循环遍历WEM部分
wemInfoList = []
for i in range(0, int(DIDX.didx_length // 12)):
    wemInfo = WEMInfo()

    # 跳转到对应的实际起始位置
    input_file.seek(didx_TruePosition + (i * 12))
    print("------------------------------------------")

    # 读取wem_id
    wemInfo.id = int.from_bytes(input_file.read(4),"little")
    print("wem_id:"+ str(wemInfo.id))

    # 读取wem_offset 这里的wem_offset指的是相对于DATA部分的偏移量
    wemInfo.offset = int.from_bytes(input_file.read(4),"little")
    print("wem_offset:"+ str(wemInfo.offset))

    # 读取wem_length
    wemInfo.length = int.from_bytes(input_file.read(4),"little")
    print("wem_bytes_length:"+ str(wemInfo.length))

    # 首先跳转到DATA部分(DATA实际起始部分 + wem偏移量)
    input_file.seek(data_TruePosition + wemInfo.offset)

    # 读取wem数据
    wemInfo.wem_bytes = input_file.read(wemInfo.length)

    # 加入列表
    wemInfoList.append(wemInfo)

# 设置WEMInfos列表
DIDX.WEMInfos = wemInfoList

# 6.读取完成后关闭文件
input_file.close()

# 7.测试写出，遍历WEMInfos列表并写出
for wemInfo in DIDX.WEMInfos:
    output_wem_file = open("C:/Users/user/Desktop/output_files/"+str(wemInfo.id)+".wem", "wb")
    output_wem_file.write(wemInfo.wem_bytes)
    output_wem_file.flush()
    output_wem_file.close()

# replace_file = open("C:/Users/user/Desktop/45593967.wem","rb")
# replace_file.close()
# output_file = open("","ab")
