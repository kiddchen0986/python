# QLabel控件使用
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette
import sys
import webbrowser


class WindowDemo(QWidget):
    def __init__(self):
        super(WindowDemo, self).__init__()
        self.label_1 = QLabel(self)
        self.label_1.setText("这是一个文本标签！<a href='www.baidu.com' style='color:red'>百度</a>")
        self.label_1.setAutoFillBackground(True)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, Qt.blue)
        self.label_1.setPalette(self.palette)
        self.label_1.setAlignment(Qt.AlignCenter)

        self.label_1.setOpenExternalLinks(True)  # 允许访问超链接
        self.label_1.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.label_1.linkActivated.connect(self.link_clicked)  # 针对链接点击事件

        self.label_2 = QLabel(self)
        self.label_2.setPixmap(QPixmap('../perception_test/2022-07-23_143321.jpg'))  # 设置图标，与文字冲突，则setText的文字不显示
        self.label_2.mousePressEvent = self.photo_link  # 设置图片点击事件
        # verification_code() takes exactly 2 arguments (1 given)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.label_1)
        self.vbox.addWidget(self.label_2)
        self.vbox.addStretch()

    def photo_link(self, test):
        webbrowser.open('https://www.baidu.com/')
        print('=====')

    def link_hovered(self):
        print("光标滑过Label_1触发事件")

    def link_clicked(self):
        print("点击时触发事件")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowDemo()
    win.show()
    sys.exit(app.exec_())