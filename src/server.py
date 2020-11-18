import json
import sys
import socket

from PyQt5.QtCore import QThread, QRect, pyqtSignal
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication, QWidget


class SocketServer(QThread):
    __slots__ = ("__saddr", "__caddr")

    callback_signal = pyqtSignal(bytes)

    def __init__(self, saddr, caddr, callback):
        super().__init__()
        self.__saddr = saddr
        self.__caddr = caddr
        self.callback_signal.connect(callback)

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.__saddr)
        server_socket.listen(10)
        print("server started")

        while True:
            connection, address = server_socket.accept()
            if self.__caddr and address[0] != self.__caddr:
                connection.close()
                continue

            with connection.makefile("rb") as fistream:
                data = fistream.read()

            connection.close()
            self.callback_signal.emit(data)


class Window(QWidget):
    __slots__ = ("__img",)

    def __init__(self, width, height):
        super().__init__()
        self.setFixedSize(width, height)
        self.__img = QImage()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.__img)

    def receive_image(self, data):
        self.__img = QImage()
        self.__img.loadFromData(data)
        self.update()


class App:
    __slots__ = ("__qapp", "__server", "__window")

    def __init__(self, saddr, caddr, rect):
        self.__qapp = QApplication([])
        self.__window = Window(*rect)
        self.__server = SocketServer(saddr, caddr, self.__window.receive_image)
        self.__window.show()

    def run(self):
        self.__server.start()
        self.__qapp.exec()


def main():
    settings_path = "./server.json"
    if len(sys.argv) >= 2:
        settings_path = sys.argv[1]

    try:
        with open(settings_path, "r") as fistream:
            data = json.load(fistream)
        App(
            saddr=(data["server"]["ip"], data["server"]["port"]),
            caddr=data["client"],
            rect=(data["rect"]["width"], data["rect"]["height"])
        ).run()

    except FileNotFoundError:
        with open(settings_path, "w") as fostream:
            json.dump(
                {
                    "server": {
                        "ip": "127.0.0.1",
                        "port": 8080},
                    "client": "127.0.0.1",
                    "rect": {
                        "width": 640,
                        "height": 480
                    }
                }, fostream)
        print("Settings file not found, new was created. Configure it")
    except KeyError as err:
        print(f"Parameter '{str(err)}' unfilled in settings file")


if __name__ == '__main__':
    main()
