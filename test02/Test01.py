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
import speech_recognition as sr
import os
def wav2txt(wavfilepath):
    r = sr.Recognizer()
    sudio = ""

    with sr.AudioFile(wavfilepath) as src:
        sudio = r.record(src)

    print(r.recognize_sphinx(sudio))


if __name__ == '__main__':
    # 测试是否能够通过本地模型读取  测试结果：不行，基本只能联网读取
    relative_path = os.path.dirname(__file__)  # 项目运行路径
    wav_path = relative_path + "\\wav\\67770531.wav"  # .cache路径

    wav2txt(wav_path)

