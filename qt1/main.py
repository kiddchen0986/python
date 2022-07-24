from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from qt1.ui_mainwindow import Ui_MainWindow
import sys
import os
import time


class MyThread(QThread):
    signal = pyqtSignal(object)

    def __init__(self):
        super(MyThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        """
        进行任务操作，主要的逻辑操作，返回结果
        """

        for pic in os.listdir('.'):
            if pic.endswith('jpg') or pic.endswith('png'):
                self.signal.emit(QtGui.QPixmap(pic))
                time.sleep(1)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # self.startButton.clicked.connect(self.buttonclicked)

    @pyqtSlot(bool)
    def on_startButton_clicked(self):
        self.thread = MyThread()
        self.thread.signal.connect(self.callback)   # 连接回调函数，接收结果
        self.thread.start()

    def callback(self, msg):
        self.perceptionlabel.setPixmap(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())