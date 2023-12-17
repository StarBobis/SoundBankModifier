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

test_wem_path = r"C:\Users\Administrator\Desktop\Test01.wem"
test_wem_file = open(test_wem_path, "rb")


class RiffChunk:
    riff_name = None
    riff_size = None
    riff_type = None

    def __str__(self):
        print("-------------RIFF Chunk-------------")
        print("riff_name: " + str(self.riff_name))
        print("riff_size: " + str(self.riff_size))
        print("riff_type: " + str(self.riff_type))
        print("------------------------------------")
class FormatChunk:
    fmt_id = None
    fmt_size = None
    fmt_tag = None
    fmt_channels = None
    fmt_samples_per_sec = None
    fmt_avg_bytes_per_sec = None
    fmt_blockalign = None
    fmt_bits_per_sample = None

    pass


# -------------RIFF CHUNK------------------
RIFF = RiffChunk()

RIFF.riff_name = test_wem_file.read(4)
RIFF.riff_size = int.from_bytes(test_wem_file.read(4), "little")
RIFF.riff_type = test_wem_file.read(4)

print(RIFF.__str__())

# -------------Format CHUNK------------------

fmt_id = test_wem_file.read(4)
print("fmt_id: " + str(fmt_id))

# 数据字段包含数据的大小。如无扩展块，则值为16；有扩展块，则值为= 16 + 2字节扩展块长度 + 扩展块长度或者值为18（只有扩展块的长度为2字节，值为0）
fmt_size = int.from_bytes(test_wem_file.read(4), "little")
print("fmt_size: " + str(fmt_size))

# 2字节，表示音频数据的格式。如值为1，表示使用PCM格式。
fmt_tag = int.from_bytes(test_wem_file.read(2), "little")
print("fmt_tag: " + str(fmt_tag))

# 2字节，声道数。值为1则为单声道，为2则是双声道。
fmt_channels = int.from_bytes(test_wem_file.read(2), "little")
print("fmt_channels: " + str(fmt_channels))

# 音频的码率，每秒播放的字节数。samples_per_sec * channels * bits_per_sample / 8，可以估算出使用缓冲区的大小
samples_per_sec = int.from_bytes(test_wem_file.read(4), "little")
print("samples_per_sec: " + str(samples_per_sec))

#
avg_bytes_per_sec = int.from_bytes(test_wem_file.read(4), "little")
print("avg_bytes_per_sec: " + str(avg_bytes_per_sec))


blockalign = int.from_bytes(test_wem_file.read(2), "little")
print("blockalign: " + str(blockalign))

bits_per_sample = int.from_bytes(test_wem_file.read(2), "little")
print("bits_per_sample: " + str(bits_per_sample))

# size = int.from_bytes(test_wem_file.read(2), "little")
# print("size: " + str(size))
#
# valid_bits_per_sample = int.from_bytes(test_wem_file.read(2), "little")
# print("valid_bits_per_sample: " + str(valid_bits_per_sample))
#
# channel_mask = int.from_bytes(test_wem_file.read(4), "little")
# print("channel_mask: " + str(channel_mask))

bits_per_sample = test_wem_file.read(10)
print("bits_per_sample: " + str(bits_per_sample))


test_wem_file.close()