import json
import sys
import socket

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QWidget


class SocketServer(QThread):
    __slots__ = ("__saddr", "__caddr")

    def __init__(self, saddr, caddr):
        super().__init__()
        self.__saddr = saddr
        self.__caddr = caddr

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.__saddr)
        server_socket.listen(10)
        print("server started")

        while True:
            connection, address = server_socket.accept()

            if address[0] == self.__caddr:
                data = connection.recv(1024)
                print(data.decode())

            connection.close()


class App:
    def __init__(self, saddr, caddr):
        self.qapp = QApplication([])
        self.server = SocketServer(saddr, caddr)
        self.window = QWidget()
        self.window.show()

    def run(self):
        self.server.start()
        self.qapp.exec()


def main():
    settings_path = "../resources/server.json"
    if len(sys.argv) >= 2:
        settings_path = sys.argv[1]

    try:
        with open(settings_path, "r") as fistream:
            data = json.load(fistream)
        App(
            saddr=(data["server"]["ip"], data["server"]["port"]),
            caddr=data["client"]
        ).run()

    except FileNotFoundError:
        with open(settings_path, "w") as fostream:
            json.dump({"server": {"ip": "127.0.0.1", "port": 8080}, "client": "127.0.0.1"}, fostream)
        print("Settings file not found, new was created. Configure it")
    except KeyError as err:
        print(f"Parameter '{str(err)}' unfilled in settings file")


if __name__ == '__main__':
    main()
