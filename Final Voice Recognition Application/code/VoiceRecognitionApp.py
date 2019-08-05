from window import Window
from datetime import datetime
from PyQt5.QtWidgets import QApplication,QMainWindow
import wave
import shutil
import pinyin
from pyaudio import PyAudio,paInt16
from aip import AipSpeech
from PIL import ImageGrab
import json
import os
import win32con
import pyaudio
import requests
import win32com
import time
import ctypes
import struct
import webbrowser
import io
import base64
import sys
import win32api
import pygame

from window import Window
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtGui


framerate=16000#采样率
NUM_SAMPLES=2000#采样点
channels=1#声道
sampwidth=2#采样宽度
FileName= 'ask.wav'

APP_ID = '16489368'
API_KEY = 'GWzEXgUIKjGh7IQDFovSItSD'
SECRET_KEY = 'MNjC7ktvtkIxwXAwxV2opGSjCGKxy8bA'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
HOST = base_url % (API_KEY, SECRET_KEY)
chunk = 1024
TURING_KEY = "111e64f1023744c9aade795df9ad72fc"
URL = "http://openapi.tuling123.com/openapi/api/v2"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}

#音量部分
WM_APPCOMMAND = 0x319

APPCOMMAND_VOLUME_MAX = 0x0a
APPCOMMAND_VOLUME_MIN = 0x09

#键值模拟

VK_CODE = {
    'a':65,
    'b':66,
    'c':67,
    'd':68,
    'e':69,
    'f':70,
    'g':71,
    'h':72,
    'i':73,
    'j':74,
    'k':75,
    'l':76,
    'm':77,
    'n':78,
    'o':79,
    'p':80,
    'q':81,
    'r':82,
    's':83,
    't':84,
    'u':85,
    'v':86,
    'w':87,
    'x':88,
    'y':89,
    'z':90
}
#speaker = win32com.client.Dispatch("SAPI.SpVoice")

def getToken(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filename,data):
    print("i am saving!")
    wf=wave.open(filename,'wb')
    print("i am saving1!")
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()

def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16,
                     channels=channels,
                     rate=framerate,
                     input=True,
                     frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    # count = 0
    t = time.time()
    print('正在录音...')

    while time.time() < t + 4:  # 秒
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)

    print('录音结束.')
    save_wave_file(FileName, my_buf)
    stream.close()

def get_file_content(filepath):
    with open(filepath, 'rb')as fp:
        return fp.read()

def speech2text(speech_data, token, dev_pid=1536):
    Result=client.asr(get_file_content(FileName),'wav',16000,{'dev_pid':dev_pid})
    print(Result)
    print("正在识别...")
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result

def speak(text=""):######################################################################
    result = client.synthesis(text, 'zh', 1, {
        'spd': 3,
        'pit':5,
        'vol': 5,
        'per': 5,
    })
    print("result:")
    print(result)
   ##########################################################################################

    timestring=datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    answerFilename = "answer"+timestring+".mp3"

    if not isinstance(result, dict):
        with open(answerFilename, 'wb') as f:
            f.write(result)

    print("AAA________")

    pygame.mixer.init()
    track = pygame.mixer.music.load(answerFilename)

    f.close()
    pygame.mixer.music.play()
    time.sleep(3)
    pygame.mixer.music.stop()
    pygame.quit()
    #os.remove(answerFilename)
    #os.unlink(answerFilename)

def fun(text):
    maps={
        '记事本':'notepad.exe',
        '音乐':'cloudmusic.exe',
        'word':'WINWORD.EXE',
       # '截屏':'TianruoOCR64.exe'
      #  '拍照':'camera.exe'
    }
    # 打开应用程序
    for command in maps.keys():
        if command in text:
            speak("即将为您打开%s" %command)
           # os.system(maps[command])
            win32api.ShellExecute(0, 'open',maps[command], '', '', 1)
            return

    # 音量调节
    if "增大音量" in text:
        speak("即将为您增大音量" )

        # 音量最大
        win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, APPCOMMAND_VOLUME_MAX * 0x10000)
        return

    elif "减小音量" in text:
        win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, APPCOMMAND_VOLUME_MIN * 0x10000)
        return

    # 网页搜索
    elif "搜索" in text:
        pos=text.index("搜索")+2
        to_find=text[pos:]
        speak("正在搜索%s" %to_find)
        print(to_find)
        webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % to_find)
        return

    # 文件寻找
    elif "寻找" in text:
        print("@@@@进入寻找")
        pos=text.index("寻找")+2
        to_find=text[pos:]
        print(to_find)
        speak("正在寻找%s" %to_find)
        # 打开右Windows键c
        win32api.keybd_event(91, 0, 0, 0)
        win32api.keybd_event(91, 0, win32con.KEYEVENTF_KEYUP, 0)
        # 模拟键盘输入（输出小写字母）
        PinYin=pinyin.get(to_find,format='strip', delimiter="")
        print(PinYin)
        time.sleep(0.8)
        for c in PinYin:
            #time.sleep(0.5)
            win32api.keybd_event(VK_CODE[c], 0, 0, 0)  # 按键
            win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            time.sleep(0.05)  # 延时1秒
        time.sleep(1)

        win32api.keybd_event(32, 0, 0, 0)  # sapcebar
        win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)

        print(to_find+"@2222")

        return

    # 截屏
    elif "截屏" in text:
        speak("正在为您截屏")
        pic=ImageGrab.grab()
        pic.save("screenshot.png")
        pic.show()
        return

    # 图灵机器人对话
    else:
        data = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": ""
                }
            },
            "userInfo": {
                "apiKey": TURING_KEY,
                "userId": "starky"
            }
        }
        data["perception"]["inputText"]["text"] = text
        response=requests.post(URL,json=data,headers=HEADERS)
        print(response)
        response_dict = json.loads(response.text)
        answer= response_dict["results"][0]["values"]["text"]
        print("the AI said: " + answer)
        speak(answer)#！！！！！！！！！！！！！！！！改！??改啥啊


class myWindow(QMainWindow, Window):

    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUI(self)

    def start_audio(self):
        self.label.setText("请说话...")
        self.label_2.setText("")
        QApplication.processEvents()
        self.show()
        my_record()
        self.label.setText("识别中")
        QApplication.processEvents()
        self.show()
        TOKEN = getToken(HOST)
        speech = get_file_content(FileName)
        result = speech2text(speech, TOKEN, 1536)

        if type(result) == str:
            self.label.setText("识别成功")
            self.label_2.setText(result)  # 这个result是文本内容,需要输出到界面上
            fun(result)
        else:
            speak('对不起,我没有听懂你在说什么')

        self.show()






if __name__ == '__main__':

    app = QApplication(sys.argv)
    mywin = myWindow()
    mywin.show()
    # flag = 'n'#按钮控制
    # flag=mywin.start_audio()
    # while flag.lower() == 'y':
    #     flag = myWindow.start_audio()
    #     my_record()
    #     TOKEN = getToken(HOST)
    #     speech = get_file_content(FileName)
    #     result = speech2text(speech, TOKEN, 1536)
    #     print(result)#这个result是文本内容,需要输出到界面上
    #     if type(result) == str:
    #         fun(result)
    #     else:
    #         speak("对不起,我没有听懂你在说什么")
    #     flag = 'n'#按钮控制
    sys.exit(app.exec_())