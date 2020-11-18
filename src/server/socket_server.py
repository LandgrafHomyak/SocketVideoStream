import socket

from PyQt5.QtCore import QThread


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
