from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from gui.abstract_view import AbstractView
from models.model_my_pull_requests import ModelMyPullRequests


class ViewMyPullRequests(QWidget, AbstractView):
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

    def refresh(self, model: ModelMyPullRequests):
        self.label.setText("gitlab")
        self.list_widget.clear()
        self.list_widget.addItem(QListWidgetItem("mr1"))
        self.list_widget.addItem(QListWidgetItem("mr2"))
