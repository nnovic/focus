from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from gui.carousel import Carousel
from gui.views.view_my_pr import ViewMyPR
from viewmodels.viewmodel_my_pr import ViewModelMyPR
from sources.gitlab.gitlab_config import GitlabConfig
from sources.gitlab.gitlab_source import GitlabSource
from focus_app import FocusApp


class MainWindow(QMainWindow):
    def __init__(self, focus_app: FocusApp):
        super().__init__()
        self._focus_app = focus_app
        self.setWindowTitle("Focus")
        self.resize(500, 350)

        # Pages
        hello = QLabel("Hello World")
        hello.setAlignment(Qt.AlignCenter)
        hello.setFont(QFont("Arial", 24))

        source = GitlabSource(config=GitlabConfig())
        source.connect()
        gitlab = ViewMyPR(model=ViewModelMyPR(model=source.get_model_my_pr()))

        carousel = Carousel([hello, gitlab])
        self.setCentralWidget(carousel)
