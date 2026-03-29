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
        list_widget = QListWidget()
        list_widget.addItem(QListWidgetItem("mr1"))
        list_widget.addItem(QListWidgetItem("mr2"))
        layout.addWidget(list_widget)

        self.setLayout(layout)

    def refresh(self, model: ModelMyPullRequests):
        self.label.setText("gitlab")
