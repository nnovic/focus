from PyQt5.QtWidgets import QMainWindow

from core.focus_app import FocusApp

from .carousel import Carousel
from .views.landing_page import LandingPage
from . import views


class MainWindow(QMainWindow):
    def __init__(self, app: FocusApp):
        super().__init__()
        self.__app = app
        self.setWindowTitle("Focus")
        self.resize(500, 350)

        # Pages
        hello = LandingPage()

        carousel = Carousel([hello])
        self.setCentralWidget(carousel)

        # Add views from config
        for view_id, view_cfg in self.__app.config.views.items():
            src = self.__app.get_source(view_cfg.source_id)
            #src.refresh()

            view_class = getattr(views, view_cfg.class_name)
            view = view_class()
            view.source_id = view_cfg.source_id

            carousel.add_view(view)
            self.__app.register_view(view_id, view)
