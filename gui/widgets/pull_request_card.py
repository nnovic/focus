from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QStyle
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

from core.scm_pull_request_descriptor import ScmPullRequestDescriptor


class PullRequestCard(QFrame):
    """A card widget displaying a pull request with icon, title, and URL."""

    def __init__(self, descriptor: ScmPullRequestDescriptor):
        super().__init__()
        self.descriptor = descriptor
        self._init_ui()

    def _init_ui(self):
        """Initialize the card UI."""
        bg_color = "#e8f5e9" if self.descriptor.is_ready_to_merge else "white"
        self.setStyleSheet(f"QFrame {{ border: 1px solid #ccc; border-radius: 12px; background-color: {bg_color}; }}")
        self.setFixedHeight(100)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon - choose based on PR status
        icon_label = QLabel()
        if self.descriptor.has_issues:
            icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
        elif self.descriptor.is_ready_to_merge:
            icon = QApplication.style().standardIcon(QStyle.SP_DialogYesButton)
        else:
            icon = QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        icon_label.setPixmap(icon.pixmap(48, 48))
        layout.addWidget(icon_label)

        # Right side: title and URL
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)

        title_label = QLabel(self.descriptor.title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setWordWrap(True)
        right_layout.addWidget(title_label)

        url_label = QLabel(self.descriptor.url or "(No URL)")
        url_label.setFont(QFont("Arial", 10))
        url_label.setStyleSheet("color: #0066cc; text-decoration: underline;")
        url_label.setWordWrap(True)
        url_label.setCursor(QCursor(Qt.PointingHandCursor))
        if self.descriptor.url:
            url_label.mousePressEvent = lambda _: QDesktopServices.openUrl(QUrl(self.descriptor.url))
        right_layout.addWidget(url_label)

        right_layout.addStretch()
        layout.addLayout(right_layout, 1)

        self.setLayout(layout)
