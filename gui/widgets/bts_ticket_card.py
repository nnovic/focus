from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QStyle
from PyQt5.QtGui import QFont, QCursor, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

from core.bts_ticket_descriptor import BtsTicketDescriptor


class BtsTicketCard(QFrame):
    def __init__(self, descriptor: BtsTicketDescriptor):
        super().__init__()
        self.descriptor = descriptor
        self._bg_color = "#f5f5f5"
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._init_ui()

    def _update_style(self, hovered: bool = False):
        """Update the card style based on hover state."""
        bg_color = self._bg_color
        if hovered:
            self.setStyleSheet(f"QFrame {{ border: 2px solid #2196F3; border-radius: 8px; background-color: {bg_color}; }}")
        else:
            self.setStyleSheet(f"QFrame {{ border: 1px solid #ddd; border-radius: 8px; background-color: {bg_color}; }}")

    def enterEvent(self, event):
        """Highlight card when mouse enters."""
        self._update_style(hovered=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Remove highlight when mouse leaves."""
        self._update_style(hovered=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Open the ticket URL in the default web browser when clicked."""
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

        # Icon container with ticket badge
        icon_container = QFrame()
        icon_container.setFixedSize(64, 64)
        icon_container_layout = QHBoxLayout()
        icon_container_layout.setContentsMargins(0, 0, 0, 0)

        # Icon - ticket icon
        icon_label = QLabel()
        icon = QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        icon_label.setPixmap(icon.pixmap(48, 48))
        icon_container_layout.addWidget(icon_label)
        icon_container.setLayout(icon_container_layout)

        # Add UUID badge
        uuid_badge = QLabel()
        uuid_badge.setText(f"#{self.descriptor.uuid}")
        uuid_badge.setFont(QFont("Arial", 9, QFont.Bold))
        uuid_badge.setStyleSheet("background-color: #E3F2FD; border-radius: 4px; padding: 2px 4px;")
        uuid_badge.setAlignment(Qt.AlignCenter)
        icon_container_layout.addWidget(uuid_badge, alignment=Qt.AlignRight | Qt.AlignBottom)

        layout.addWidget(icon_container)

        # Right side: title and metadata
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)

        title_label = QLabel(self.descriptor.title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setWordWrap(True)
        right_layout.addWidget(title_label)

        # Date label if available
        if self.descriptor.created_at:
            date_label = QLabel(f"Created: {self.descriptor.created_at.strftime('%Y-%m-%d')}")
            date_label.setFont(QFont("Arial", 9))
            date_label.setStyleSheet("color: #888;")
            right_layout.addWidget(date_label)

        right_layout.addStretch()
        layout.addLayout(right_layout, 1)

        self.setLayout(layout)
