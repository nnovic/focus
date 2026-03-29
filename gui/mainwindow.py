from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .carousel import Carousel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus")
        self.resize(500, 350)

        # Pages
        hello = QLabel("Hello World")
        hello.setAlignment(Qt.AlignCenter)
        hello.setFont(QFont("Arial", 24))

        gitlab = QLabel("gitlab")
        gitlab.setAlignment(Qt.AlignCenter)
        gitlab.setFont(QFont("Arial", 24))

        carousel = Carousel([hello, gitlab])
        self.setCentralWidget(carousel)
