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
# 测试获取相对路径
import os
import shutil
from SoundBankUtil import  *




shell_text = testexe_path + ' -o ' + output_wav_file + ' ' + input_wem_file
decode_process = subprocess.Popen(shell_text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  encoding='gb2312')
print(decode_process.communicate()[0])