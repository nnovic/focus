from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.focus_app import FocusApp


from .carousel import Carousel
from . import views


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

        carousel = Carousel([hello])
        self.setCentralWidget(carousel)

        # Add views from config
        for view_id, view_cfg in self.__app.config.views.items():
            src = self.__app.get_source(view_cfg.source_id)
            #src.refresh()

            view_class = getattr(views, view_cfg.class_name)
            view = view_class()
            view.source_id = view_cfg.source_id

            # Try each preferred model type until one is available
            for model_class in view.best_models:
                model = src.get_model(model_class)
                if model is not None:
                    view.refresh(model)
                    carousel.add_view(view)
                    break

        # Refresh sources
        for src_id in self.__app.sources:
            src = self.__app.get_source(src_id)
            src.refresh()

        # Refresh views
        for view in carousel.views:
            src_id = view.source_id
            src = self.__app.get_source(src_id)

            # Try each preferred model type until one is available
            for model_class in view.best_models:
                model = src.get_model(model_class)
                if model is not None:
                    view.refresh(model)
                    break

        pass
