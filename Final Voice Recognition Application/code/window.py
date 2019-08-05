from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie,QIcon
from PyQt5.QtWidgets import QPushButton,QTextEdit
import pyaudio


class Window(object):
    def setupUI(self,MainWindow):
        #界面背景设为黑色，大小待更改
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 600)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #显示动图,需要更改位置
        self.picture = QtWidgets.QLabel(self.centralwidget)
        self.picture.setGeometry(QtCore.QRect(25, 400, 400, 121))
        self.picture.setText("")
        self.gif = QMovie("timg2.gif")
        self.picture.setMovie(self.gif)
        self.gif.start()
        self.picture.setScaledContents(True)
        self.picture.setObjectName("picture")

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(200, 500, 50, 50))
        self.startButton.setIconSize(QtCore.QSize(50, 50))
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.start_audio)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("start.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(icon2)
        self.startButton.setIconSize(QtCore.QSize(50, 50))

        #label用来显示状态，是输入中，识别中、、、、，更改位置
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 50, 400, 70))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 117, 210);")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.setText("Hello, you can push the start button to begin")

        # label_2用来显示输入的内容,需要更改位置
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 400, 70))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_2.setText(" ")




        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))

