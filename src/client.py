#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Графический PyQt 5 клиент для работы с сервером чата
import sys
from PyQt5 import QtWidgets
from gui import design

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver


class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Connector'

    def connectionMade(self):
        self.factory.window.protocol = self
        self.factory.window.plainTextEdit.appendPlainText("Connected")

    def lineReceived(self, line):  # call connection
        message = line.decode()
        self.factory.window.plainTextEdit.appendPlainText(message)


class Connector(ClientFactory):
    window: 'ChatWindow'
    protocol = ConnectorProtocol

    def __init__(self, app_window) -> None:
        self.window = app_window


class ChatWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    reactor = None
    protocol = ConnectorProtocol

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def send_message(self):
        message = self.lineEdit.text()
        self.protocol.sendLine(message.encode())
        self.lineEdit.setText("")

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)


app = QtWidgets.QApplication(sys.argv)

import qt5reactor

window = ChatWindow()
window.show()

qt5reactor.install()

from twisted.internet import reactor

reactor.connectTCP(
    "localhost",
    1234,
    Connector(window)
)

window.reactor = reactor
reactor.run()
