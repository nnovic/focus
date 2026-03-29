from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from viewmodels.viewmodel_my_pr import ViewModelMyPR


class ViewMyPR(QWidget):
    def __init__(self, model: ViewModelMyPR, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel(model.title)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24))

        mr_title = QLabel("My merge request")
        mr_title.setFont(QFont("Arial", 14, QFont.Bold))

        mr_list = QListWidget()
        mr_list.addItems(model.pr_names_list)

        layout.addWidget(title)
        layout.addWidget(mr_title)
        layout.addWidget(mr_list)
