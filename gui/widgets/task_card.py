from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QStyle
from PyQt5.QtGui import QFont, QCursor, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

from core.generic_task_descriptor import GenericTaskDescriptor


class TaskCard(QFrame):
    def __init__(self, descriptor: GenericTaskDescriptor):
        super().__init__()
        self.descriptor = descriptor
        self._bg_color = self._get_background_color()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._init_ui()

    def _get_background_color(self) -> str:
        """Get the background color based on priority."""
        priority = self.descriptor.priority
        if priority >= 80:
            return "#e8f5e9"  # Green for high priority
        elif priority >= 60:
            return "#fff3e0"  # Orange for medium priority
        else:
            return "white"    # White for low priority

    def _update_style(self, hovered: bool = False):
        """Update the card style based on hover state."""
        bg_color = self._bg_color
        if hovered:
            opacity = "dd"
            bg_color += opacity if len(self._bg_color) == 7 else ""
            self.setStyleSheet(f"QFrame {{ border: 1px solid #999; border-radius: 12px; background-color: {bg_color}; }}")
        else:
            self.setStyleSheet(f"QFrame {{ border: 1px solid #ccc; border-radius: 12px; background-color: {bg_color}; }}")

    def enterEvent(self, event):
        """Highlight card when mouse enters."""
        self._update_style(hovered=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Remove highlight when mouse leaves."""
        self._update_style(hovered=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Open the task URL in the default web browser when clicked."""
        if self.descriptor.url:
            QDesktopServices.openUrl(QUrl(self.descriptor.url))
        super().mousePressEvent(event)

    def _init_ui(self):
        """Initialize the card UI."""
        self._update_style(hovered=False)
        self.setFixedHeight(100)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon container with priority badge
        icon_container = QFrame()
        icon_container.setFixedSize(64, 64)
        icon_container_layout = QHBoxLayout()
        icon_container_layout.setContentsMargins(0, 0, 0, 0)

        # Icon - task icon
        icon_label = QLabel()
        icon = QApplication.style().standardIcon(QStyle.SP_DialogYesButton)
        icon_label.setPixmap(icon.pixmap(48, 48))
        icon_container_layout.addWidget(icon_label)
        icon_container.setLayout(icon_container_layout)

        # Add priority badge
        priority_badge = QLabel()
        priority_badge.setText(f"⚡ {self.descriptor.priority}")
        priority_badge.setFont(QFont("Arial", 9, QFont.Bold))
        priority_badge.setStyleSheet("background-color: #FFD700; border-radius: 6px; padding: 2px 4px;")
        priority_badge.setAlignment(Qt.AlignCenter)
        icon_container_layout.addWidget(priority_badge, alignment=Qt.AlignRight | Qt.AlignBottom)

        layout.addWidget(icon_container)

        # Right side: title and description
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)

        title_label = QLabel(self.descriptor.title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setWordWrap(True)
        right_layout.addWidget(title_label)

        description_label = QLabel(self.descriptor.description)
        description_label.setFont(QFont("Arial", 10))
        description_label.setStyleSheet("color: #666;")
        description_label.setWordWrap(True)
        right_layout.addWidget(description_label)

        right_layout.addStretch()
        layout.addLayout(right_layout, 1)

        self.setLayout(layout)
