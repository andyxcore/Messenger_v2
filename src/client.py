from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
import sys
from PyQt5 import QtWidgets
import design


class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Connector'

    def connectionMade(self):
        self.factory.window.protocol = self
        self.factory.window.plainTextEdit.appendPlainText("Connected")

    def lineReceived(self, line):
        message = line.decode()
        self.factory.window.plainTextEdit(message)


class Connector(ClientFactory):
    protocol = ConnectorProtocol
    window: 'ChatWindow'

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window


class ChatWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    reactor = None
    protocol: ConnectorProtocol

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        message = self.lineEdit.text()
        # self.plainTextEdit.appendPlainText(message)
        self.protocol.sendLine(message.encode())
        self.lineEdit.setText('')


app = QtWidgets.QApplication(sys.argv)

import qt5reactor

window = ChatWindow()
window.show()

qt5reactor.install()

#from twisted.internet import reactor

reactor.connectTCP("localhost", 1234, Connector(window))

window.reactor = reactor
reactor.run()
