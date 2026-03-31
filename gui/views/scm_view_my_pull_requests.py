from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.scm_model_my_pull_requests import ScmModelMyPullRequests
from .abstract_view import AbstractView


class ScmViewMyPullRequests(AbstractView, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 24))
        layout.addWidget(self.label)

        # List
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    @property
    def best_models(self) -> list[type]:
        return [ScmModelMyPullRequests]

    def refresh(self, model: ScmModelMyPullRequests):
        self.label.setText(model.title)
        self.list_widget.clear()
        
        for desc in model.pull_requests:
            text = str(desc.priority) + "---" + desc.title
            self.list_widget.addItem(QListWidgetItem(text))
