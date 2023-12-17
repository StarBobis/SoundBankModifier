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

# 测试使用google进行普通话识别
# 项目运行路径
relative_path = os.path.dirname(__file__)
# wav文件路径
wav_path = relative_path + "\\wav\\358717481.wav"

# 调用识别器
r = sr.Recognizer()

audio = ""
with sr.AudioFile(wav_path) as source:
    audio = r.record(source)

print(r.recognize_google(audio, language='zh-CN'))




