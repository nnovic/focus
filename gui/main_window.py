from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.focus_app import FocusApp
from core.scm_model_my_pull_requests import ScmModelMyPullRequests
from sources.gitlab.gitlab_models import GitlabModelMyPullRequests
from sources.gitlab.gitlab_source import GitlabSource


from .carousel import Carousel
from .views import ScmViewMyPullRequests


class MainWindow(QMainWindow):
    def __init__(self, app: FocusApp):
        super().__init__()
        self.__app = app
        self.setWindowTitle("Focus")
        self.resize(500, 350)

        # Pages
        hello = QLabel("Hello World")
        hello.setAlignment(Qt.AlignCenter)
        hello.setFont(QFont("Arial", 24))

        cfg = self.__app.config.get_source_config("1")
        gl = GitlabSource()
        gl.configure(cfg)
        gl.connect()
        gl.refresh()

        model = gl.get_model(ScmModelMyPullRequests)

        gitlab = ScmViewMyPullRequests()
        gitlab.refresh(model)

        carousel = Carousel([hello, gitlab])
        self.setCentralWidget(carousel)
