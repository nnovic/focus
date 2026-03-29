import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont
from gui.views.view_my_pr import ViewMyPR
from viewmodels.viewmodel_my_pr import ViewModelMyPR
from sources.gitlab.gitlab_model_my_pr import GitlabModelMyPR


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

    def _update_ui(self):
        self._btn_prev.setEnabled(self._current > 0)
        self._btn_next.setEnabled(self._current < len(self._pages) - 1)
        for i, dot in enumerate(self._dots):
            dot.setStyleSheet("color: #333;" if i == self._current else "color: #bbb;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus")
        self.resize(500, 350)

        # Pages
        hello = QLabel("Hello World")
        hello.setAlignment(Qt.AlignCenter)
        hello.setFont(QFont("Arial", 24))

        gitlab = ViewMyPR(model=ViewModelMyPR(model=GitlabModelMyPR()))

        carousel = Carousel([hello, gitlab])
        self.setCentralWidget(carousel)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
