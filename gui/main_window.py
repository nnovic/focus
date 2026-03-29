from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from sources.gitlab.gitlab_model_my_pull_requests import GitlabModelMyPullRequests

from .carousel import Carousel
from .views import ViewMyPullRequests


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus")
        self.resize(500, 350)

        # Pages
        hello = QLabel("Hello World")
        hello.setAlignment(Qt.AlignCenter)
        hello.setFont(QFont("Arial", 24))

        gitlab = ViewMyPullRequests()
        model = GitlabModelMyPullRequests()
        gitlab.refresh(model)

        carousel = Carousel([hello, gitlab])
        self.setCentralWidget(carousel)
