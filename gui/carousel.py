from PyQt5.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont


class Carousel(QWidget):
    def __init__(self, pages: list[QWidget], parent=None):
        super().__init__(parent)
        self._pages = pages
        self._current = 0

        # Stacked widget holds all pages
        self._stack = QStackedWidget()
        for page in pages:
            self._stack.addWidget(page)

        # Navigation buttons
        self._btn_prev = QPushButton("‹")
        self._btn_next = QPushButton("›")
        for btn in (self._btn_prev, self._btn_next):
            btn.setFixedSize(40, 40)
            btn.setFont(QFont("Arial", 20))
            btn.setCursor(Qt.PointingHandCursor)

        self._btn_prev.clicked.connect(self._go_prev)
        self._btn_next.clicked.connect(self._go_next)

        # Dot indicators
        self._dots: list[QLabel] = []
        dots_layout = QHBoxLayout()
        dots_layout.setAlignment(Qt.AlignCenter)
        for _ in range(len(pages)):
            dot = QLabel("●")
            dot.setAlignment(Qt.AlignCenter)
            self._dots.append(dot)
            dots_layout.addWidget(dot)

        # Main row: prev | stack | next
        row = QHBoxLayout()
        row.addWidget(self._btn_prev)
        row.addWidget(self._stack, stretch=1)
        row.addWidget(self._btn_next)

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addLayout(dots_layout)

        self._update_ui()

    def _go_prev(self):
        if self._current > 0:
            self._slide_to(self._current - 1, direction=-1)

    def _go_next(self):
        if self._current < len(self._pages) - 1:
            self._slide_to(self._current + 1, direction=1)

    def _slide_to(self, index: int, direction: int):
        width = self._stack.width()
        current_widget = self._stack.currentWidget()
        next_widget = self._pages[index]

        # Position next widget off-screen
        next_widget.setGeometry(direction * width, 0, width, self._stack.height())
        next_widget.show()

        # Animate current out
        anim_out = QPropertyAnimation(current_widget, b"geometry")
        anim_out.setDuration(300)
        anim_out.setStartValue(current_widget.geometry())
        anim_out.setEndValue(QRect(-direction * width, 0, width, self._stack.height()))
        anim_out.setEasingCurve(QEasingCurve.OutCubic)

        # Animate next in
        anim_in = QPropertyAnimation(next_widget, b"geometry")
        anim_in.setDuration(300)
        anim_in.setStartValue(QRect(direction * width, 0, width, self._stack.height()))
        anim_in.setEndValue(QRect(0, 0, width, self._stack.height()))
        anim_in.setEasingCurve(QEasingCurve.OutCubic)

        self._stack.setCurrentIndex(index)
        self._current = index
        self._update_ui()

        anim_out.start()
        anim_in.start()

        # Keep references alive until animation finishes
        self._anims = (anim_out, anim_in)

    def add_page(self, page: QWidget):
        """Add a page to the carousel after creation."""
        self._pages.append(page)
        self._stack.addWidget(page)

        # Add a new dot indicator
        dot = QLabel("●")
        dot.setAlignment(Qt.AlignCenter)
        self._dots.append(dot)
        # Find the dots layout and add the new dot
        dots_layout = self.layout().itemAt(1).layout()
        dots_layout.addWidget(dot)

        self._update_ui()

    def _update_ui(self):
        self._btn_prev.setEnabled(self._current > 0)
        self._btn_next.setEnabled(self._current < len(self._pages) - 1)
        for i, dot in enumerate(self._dots):
            dot.setStyleSheet("color: #333;" if i == self._current else "color: #bbb;")
