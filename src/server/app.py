from PyQt5.QtWidgets import QApplication, QWidget

from socket_server import SocketServer


class App:
    def __init__(self, saddr, caddr):
        self.qapp = QApplication([])
        self.server = SocketServer(saddr, caddr)
        self.window = QWidget()
        self.window.show()

    def run(self):
        self.server.start()
        self.qapp.exec()
