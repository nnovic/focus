from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter
from pathlib import Path


class LandingPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Load background image
        bg_path = Path(__file__).parent / "welcome_background.png"
        self.background = QPixmap(str(bg_path))

        # Create title label
        title = QLabel("Focus")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24))
        title.setStyleSheet("background-color: transparent;")

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_bg = self.background.scaledToWidth(self.width(), Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_bg)
        super().paintEvent(event)
