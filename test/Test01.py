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

# Test01 测试读取BNK文件，并解压为单独的wem文件
input_file = open("C:/Users/user/Desktop/dialogue_outgame_tarka.bnk","rb")
print("开始读取文件，当前指针位置："+str(input_file.tell()))

# 读取BKHD标识，是4个字节
bkhd_section = input_file.read(4)

if(bkhd_section == b'BKHD'):
    print("检测到BNK文件，当前指针位置："+str(input_file.tell()))

# seek()用来移动文件指针到指定位置
# 读取BKHD剩余部分的长度数值，也是4个字节
bkhd_length = int.from_bytes(input_file.read(4),"little")
# int.from_bytes(bytes,"") 第二个参数填little就是littleEndian，填big就是BigEndian
print("bkhd_length:"+str(bkhd_length))
print("当前指针位置："+str(input_file.tell()))

# 跳过bkhd部分，进入DIDX部分
input_file.seek(bkhd_length+4+4)
didx_section = input_file.read(4)
print("检测到DIDX部分，当前指针位置："+ str(input_file.tell()))

# 获取DIDX部分的长度
didx_length = int.from_bytes(input_file.read(4),"little")
didx_position = input_file.tell()
print("didx_length:"+str(didx_length))

# 获取DIDX部分结束位置
data_section_position = int(input_file.tell()) + didx_length
print("data_section_position:"+str(data_section_position))
input_file.seek(data_section_position)

data_section = input_file.read(4)
print(data_section)
data_length = int.from_bytes(input_file.read(4),"little")
print("data_length:"+str(data_length))
data_start_position = input_file.tell()

# 恢复到DIDX部分

for i in range(0 ,int(didx_length // 12)):
    print("------------------------------------------")
    input_file.seek(didx_position + (i * 12))



    wem_id = int.from_bytes(input_file.read(4),"little")
    print("wem_id:"+ str(wem_id))

    # 这里的wem_offset指的是相对于DATA部分的偏移量
    wem_offset = int.from_bytes(input_file.read(4),"little")
    print("wem_offset:"+ str(wem_offset))

    wem_bytes_length = int.from_bytes(input_file.read(4),"little")
    print("wem_bytes_length:"+ str(wem_bytes_length))

    # 这里测试写出读取到的第一个wem文件
    # 首先跳转到DATA部分(DATA起始部分 + wem偏移量)
    input_file.seek(data_start_position + wem_offset)

    # 读取wem数据
    wem_bytes = input_file.read(wem_bytes_length)

    output_wem_file = open("C:/Users/user/Desktop/output_files/"+str(wem_id)+".wem","wb")

    output_wem_file.write(wem_bytes)
    output_wem_file.flush()
    output_wem_file.close()

# num2 = hex(100) * input_file.read(1)
# num3 = hex(10000) * input_file.read(1)
# num4 = hex(1000000) * input_file.read(1)

# 读取完成后关闭文件
input_file.close()

# output_file = open("","ab")
