from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.scm_model_my_pull_requests import ScmModelMyPullRequests
from gui.views.concrete_view import ConcreteView
from gui.widgets.pull_request_card import PullRequestCard
from .abstract_view import AbstractView


class ScmViewMyPullRequests(ConcreteView):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        # Title label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 24))
        main_layout.addWidget(self.label)

        # Scrollable grid area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.grid_container = QWidget()
        self.grid_layout = QVBoxLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_container.setLayout(self.grid_layout)

        self.scroll_area.setWidget(self.grid_container)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    @property
    def best_models(self) -> list[type]:
        return [ScmModelMyPullRequests]

    def refresh(self, model: ScmModelMyPullRequests):
        self.label.setText(model.title)

        # Clear grid
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add cards in 2-column layout
        row = QHBoxLayout()
        row.setSpacing(10)

        for i, desc in enumerate(model.pull_requests):
            card = PullRequestCard(desc)
            row.addWidget(card)

            # Every 2 cards, start a new row
            if (i + 1) % 2 == 0:
                row_widget = QWidget()
                row_widget.setLayout(row)
                self.grid_layout.addWidget(row_widget)
                row = QHBoxLayout()
                row.setSpacing(10)

        # Add remaining cards if odd number
        if len(model.pull_requests) % 2 != 0:
            row.addStretch()
            row_widget = QWidget()
            row_widget.setLayout(row)
            self.grid_layout.addWidget(row_widget)

        self.grid_layout.addStretch()
