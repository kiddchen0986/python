from PyQt5.QtWidgets import QMainWindow, QApplication
from qt1.usd2rmb.ui_usd2rmb import Ui_MainWindow
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.transferpushButton.clicked.connect(self.buttonclicked)

    def buttonclicked(self):
        input = self.usdlineEdit.text()
        output = float(input) * 6.7
        self.rmblineEdit.setText(str(output))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())