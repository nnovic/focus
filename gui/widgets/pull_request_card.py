from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QStyle
from PyQt5.QtGui import QFont, QCursor, QPixmap, QPainter
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

from core.scm_pull_request_descriptor import ScmPullRequestDescriptor


class PullRequestCard(QFrame):
    def __init__(self, descriptor: ScmPullRequestDescriptor):
        super().__init__()
        self.descriptor = descriptor
        self._bg_color = self._get_background_color()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._init_ui()

    def _get_background_color(self) -> str:
        """Get the background color based on PR status."""
        if self.descriptor.has_issues:
            return "#ffebee"
        elif self.descriptor.is_ready_to_merge:
            return "#e8f5e9"
        else:
            return "white"

    def _get_icon(self):
        """Get the icon based on PR status."""
        if self.descriptor.has_issues:
            return QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
        elif self.descriptor.is_ready_to_merge:
            return QApplication.style().standardIcon(QStyle.SP_DialogYesButton)
        else:
            return QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)

    def _update_style(self, hovered: bool = False):
        """Update the card style based on hover state."""
        bg_color = self._bg_color
        if hovered:
            # Darken the background slightly on hover
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
        """Open the PR URL in the default web browser when clicked."""
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

        # Icon container with upvotes badge (layered)
        icon_container = QFrame()
        icon_container.setFixedSize(64, 64)

        # Icon - choose based on PR status
        icon_label = QLabel(icon_container)
        icon = self._get_icon()
        icon_label.setPixmap(icon.pixmap(48, 48))
        icon_label.setGeometry(8, 8, 48, 48)

        # Add upvotes badge if >= 1 (on top layer)
        if self.descriptor.upvotes >= 1:
            upvotes_badge = QLabel(icon_container)
            upvotes_badge.setText(f"👍 {self.descriptor.upvotes}")
            upvotes_badge.setFont(QFont("Arial", 9, QFont.Bold))
            upvotes_badge.setStyleSheet("background-color: #FFD700; border-radius: 6px; padding: 2px 4px;")
            upvotes_badge.setAlignment(Qt.AlignCenter)
            upvotes_badge.setGeometry(32, 40, 32, 20)

        layout.addWidget(icon_container)

        # Right side: title and URL
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)

        title_label = QLabel(self.descriptor.title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setWordWrap(True)
        right_layout.addWidget(title_label)

        url_label = QLabel(self.descriptor.url or "(No URL)")
        url_label.setFont(QFont("Arial", 10))
        url_label.setStyleSheet("color: #0066cc;")
        url_label.setWordWrap(True)
        right_layout.addWidget(url_label)

        # Add days_old information
        if self.descriptor.days_old is not None:
            days_old_label = QLabel(f"📅 {self.descriptor.days_old} days old")
            days_old_label.setFont(QFont("Arial", 9))
            days_old_label.setStyleSheet("color: #666; margin-top: 5px;")
            right_layout.addWidget(days_old_label)

        right_layout.addStretch()
        layout.addLayout(right_layout, 1)

        self.setLayout(layout)
