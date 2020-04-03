import sys
from PyQt5 import QtWidgets
import design


class ChatWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def send_message(self):
        message = self.lineEdit.text()
        self.plainTextEdit.appendPlainText(message)
        self.lineEdit.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
