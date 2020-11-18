from PyQt5.QtWidgets import QApplication, QWidget


class App:
    def __init__(self, ip, port):
        self.qapp = QApplication([])
        self.window = QWidget()
        self.window.show()
        self.qapp.exec()