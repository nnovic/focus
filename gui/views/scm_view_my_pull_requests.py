from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.scm_model_my_pull_requests import ScmModelMyPullRequests
from gui.views.concrete_view import ConcreteView
from gui.widgets.pull_request_card import PullRequestCard
from gui.widgets.flow_layout import FlowLayout
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

        # Scrollable flow layout area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.flow_container = QWidget()
        self.flow_layout = FlowLayout()
        self.flow_layout.setSpacing(15)
        self.flow_layout.setContentsMargins(10, 10, 10, 10)
        self.flow_container.setLayout(self.flow_layout)

        self.scroll_area.setWidget(self.flow_container)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    @property
    def best_models(self) -> list[type]:
        return [ScmModelMyPullRequests]

    def refresh(self, model: ScmModelMyPullRequests):
        self.label.setText(model.title)

        # Clear flow layout
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add cards to flow layout
        for desc in model.pull_requests:
            card = PullRequestCard(desc)
            card.setFixedSize(400, 100)
            self.flow_layout.addWidget(card)
