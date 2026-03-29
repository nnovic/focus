from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ViewMyPR(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("gitlab")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24))

        mr_title = QLabel("merge request")
        mr_title.setFont(QFont("Arial", 14, QFont.Bold))

        mr_list = QListWidget()
        mr_list.addItems(["mr1", "mr2"])

        layout.addWidget(title)
        layout.addWidget(mr_title)
        layout.addWidget(mr_list)
