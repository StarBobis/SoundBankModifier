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


class RiffChunk:
    riff_name = None
    riff_size = None
    riff_from_type = None

    def __str__(self):
        print("-------------RIFF Chunk----------------")
        print("riff_name: " + str(self.riff_name))
        print("riff_size: " + str(self.riff_size))
        print("riff_from_type: " + str(self.riff_from_type))
        print("RIFF Chunk总占用大小：12")
        print("---------------------------------------")


class FormatChunkNoExtend:
    fmt_id = None
    fmt_size = None  # 数据字段包含数据的大小。如无扩展块，则值为16；有扩展块，则值为= 16 + 2字节扩展块长度 + 扩展块长度或者值为18（只有扩展块的长度为2字节，值为0）
    fmt_tag = None  # 2字节，表示音频数据的格式。如值为1，表示使用PCM格式。 测试读取值为65535，所以foobar2000无法识别是哪种类型的vorbis
    fmt_channels = None  # 2字节，声道数。值为1则为单声道，为2则是双声道。
    fmt_samples_per_sec = None  # 音频的码率，每秒播放的字节数。samples_per_sec * channels * bits_per_sample / 8，可以估算出使用缓冲区的大小
    fmt_avg_bytes_per_sec = None
    fmt_blockalign = None
    fmt_bits_per_sample = None

    def __str__(self):
        print("-------------Format  Chunk-------------(NoExtend)")
        print("fmt_id: " + str(self.fmt_id))
        print("fmt_size: " + str(self.fmt_size))
        print("fmt_tag: " + str(self.fmt_tag))
        print("fmt_channels: " + str(self.fmt_channels))
        print("fmt_samples_per_sec: " + str(self.fmt_samples_per_sec))
        print("fmt_avg_bytes_per_sec: " + str(self.fmt_avg_bytes_per_sec))
        print("fmt_blockalign: " + str(self.fmt_blockalign))
        print("fmt_bits_per_sample: " + str(self.fmt_bits_per_sample))
        print("---------------------------------------")


class FormatChunkExtend:
    fmt_id = None
    fmt_size = None  # 数据字段包含数据的大小。如无扩展块，则值为16；有扩展块，则值为= 16 + 2字节扩展块长度 + 扩展块长度或者值为18（只有扩展块的长度为2字节，值为0）
    fmt_tag = None  # 2字节，表示音频数据的格式。如值为1，表示使用PCM格式。 测试读取值为65535，所以foobar2000无法识别是哪种类型的vorbis
    fmt_channels = None  # 2字节，声道数。值为1则为单声道，为2则是双声道。
    fmt_samples_per_sec = None  # 音频的码率，每秒播放的字节数。samples_per_sec * channels * bits_per_sample / 8，可以估算出使用缓冲区的大小
    fmt_avg_bytes_per_sec = None
    fmt_blockalign = None
    fmt_bits_per_sample = None
    fmt_cb_size = None  # 扩展区长度


    def __str__(self):
        print("-------------Format  Chunk-------------(Extend)")
        print("fmt_id: " + str(self.fmt_id))
        print("fmt_size: " + str(self.fmt_size))
        print("fmt_tag: " + str(self.fmt_tag))
        print("fmt_channels: " + str(self.fmt_channels))
        print("fmt_samples_per_sec: " + str(self.fmt_samples_per_sec))
        print("fmt_avg_bytes_per_sec: " + str(self.fmt_avg_bytes_per_sec))
        print("fmt_blockalign: " + str(self.fmt_blockalign))
        print("fmt_bits_per_sample: " + str(self.fmt_bits_per_sample))
        print("fmt_cb_size: " + str(self.fmt_cb_size))
        print("---------------------------------------")

class SubChunk:
    sub_id = None
    sub_size = None
    sub_data = None

class DataChunk:
    data_id = None
    data_size = None
    data_bytes = None

    def __str__(self):
        print("---------------Data  Chunk-------------")
        print("data_id: " + str(self.data_id))
        print("data_size: " + str(self.data_size))
        # print("data_bytes: " + str(self.data_bytes))
        print("---------------------------------------")


def main():
    # 初始化路径
    test_wem_path = r"C:\Users\Administrator\Desktop\Test02.wem"

    # 打开wem文件
    test_wem_file = open(test_wem_path, "rb")

    # 打印总字节数
    wem_file_size = os.path.getsize(test_wem_path)
    print("wem_file_size: " + str(wem_file_size))

    # -------------RIFF CHUNK------------------
    RIFF = RiffChunk()

    RIFF.riff_name = test_wem_file.read(4)
    RIFF.riff_size = int.from_bytes(test_wem_file.read(4), "little")
    RIFF.riff_from_type = test_wem_file.read(4)

    RIFF.__str__()

    # -------------Format CHUNK------------------
    FMT = FormatChunkExtend()

    FMT.fmt_id = test_wem_file.read(4)
    FMT.fmt_size = int.from_bytes(test_wem_file.read(4), "little")
    FMT.fmt_tag = int.from_bytes(test_wem_file.read(2), "little")
    FMT.fmt_channels = int.from_bytes(test_wem_file.read(2), "little")
    FMT.fmt_samples_per_sec = int.from_bytes(test_wem_file.read(4), "little")
    FMT.fmt_avg_bytes_per_sec = int.from_bytes(test_wem_file.read(4), "little")
    FMT.fmt_blockalign = int.from_bytes(test_wem_file.read(2), "little")
    FMT.fmt_bits_per_sample = int.from_bytes(test_wem_file.read(2), "little")
    FMT.fmt_cb_size = int.from_bytes(test_wem_file.read(2), "little")

    FMT.__str__()

    # extend_size = int.from_bytes(test_wem_file.read(2), "little")  # 扩展区的数据长度 ，可以为0或22，为0说明没有扩展区内容
    # print("extend_size: " + str(extend_size))

    valid_bits_per_sample = int.from_bytes(test_wem_file.read(2), "little")
    # 有效的采样位数，最大值为采样字节数 * 8。可以使用更灵活的量化位数，通常音频sample的量化位数为8的倍数，
    # 但是使用了WAVE_FORMAT_EXTENSIBLE时，量化的位数有扩展区中的valid bits per sample来描述，可以小于Format chunk中制定的bits per sample
    print("valid_bits_per_sample: " + str(valid_bits_per_sample))
    # channel_mask = int.from_bytes(test_wem_file.read(4),"little")  # 声道掩码 4字节
    channel_mask = test_wem_file.read(4)  # 声道掩码 4字节
    print("channel_mask: " + str(channel_mask))
    #
    # sub_format = test_wem_file.read(16)  # GUID，include the data format code，数据格式码。
    # print("sub_format: " + str(sub_format))

    sub_format = test_wem_file.read(42)  # GUID，include the data format code，数据格式码。
    print("sub_format: " + str(sub_format))

    # ---------------Data CHUNK------------------
    DATA = DataChunk()
    DATA.data_id = test_wem_file.read(4)
    DATA.data_size = int.from_bytes(test_wem_file.read(4), "little")  #49588
    DATA.data_bytes = test_wem_file.read(wem_file_size - test_wem_file.tell())

    DATA.__str__()


    #




    test_wem_file.close()


if __name__ == '__main__':
    main()

