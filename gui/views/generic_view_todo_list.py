from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from core.generic_model_todo_list import GenericModelTodoList
from gui.views.concrete_view import ConcreteView
from gui.widgets.task_card import TaskCard
from gui.widgets.flow_layout import FlowLayout
from .abstract_view import AbstractView


class GenericViewTodoList(ConcreteView):
    refresh_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.refresh_signal.connect(self._on_refresh)
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
        return [GenericModelTodoList]

    def refresh(self, model: GenericModelTodoList):
        self.refresh_signal.emit(model)

    def _on_refresh(self, model: GenericModelTodoList):
        print(f"GenericViewTodoList.refresh called with {len(model.tasks)} tasks")
        self.label.setText(model.title)

        # Clear flow layout
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add cards to flow layout
        for desc in model.tasks:
            card = TaskCard(desc)
            card.setFixedSize(400, 100)
            self.flow_layout.addWidget(card)

        self.flow_layout.update()
        self.flow_container.update()
        self.scroll_area.viewport().update()
