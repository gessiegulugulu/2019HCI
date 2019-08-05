from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QToolBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from asrInterface import Ui_MainWindow
import sys
import win32api

import speech_recognition as sr


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def recognize_speech_from_mic(recognizer, microphone):
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command=recognizer.recognize_sphinx(audio)

        return command


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()

    print("Begin speaking")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    phrase = myWindow.recognize_speech_from_mic(recognizer,microphone)

    print(phrase)


    if "play music" in phrase:
        win32api.ShellExecute(0, 'open', 'E:\\song.wma', '','',1)
    elif "playing music" in phrase:
        win32api.ShellExecute(0, 'open', 'E:\\song.wma', '', '', 1)
    elif "open note pad" in phrase:
        win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)
    elif "open notepad" in phrase:
        win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)


    sys.exit(app.exec())


