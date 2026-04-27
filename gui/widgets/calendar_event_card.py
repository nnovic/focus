from datetime import datetime
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTime, QUrl
from PyQt5.QtGui import QDesktopServices

from core.calendar_event_descriptor import CalendarEventDescriptor
from gui.widgets.concrete_card import ConcreteCard


class CalendarEventCard(ConcreteCard):
    def __init__(self, descriptor: CalendarEventDescriptor):
        super().__init__()
        self.descriptor = descriptor
        now = datetime.now()
        end = descriptor.end_time.replace(tzinfo=None)
        start = descriptor.start_time.replace(tzinfo=None)
        if end < now:
            self._bg_color = "#e0e0e0"  # terminated: gray
        elif start <= now <= end:
            self._bg_color = "#bbdefb"  # in progress: blue
        elif (start - now).total_seconds() < 15 * 60:
            self._bg_color = "#ffe0b2"  # starting soon: orange
        else:
            self._bg_color = "#f5f5f5"  # upcoming: default
        self._duration_label = None
        self._location_label = None
        self._init_ui()
        self.setFixedHeight(100)

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

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.descriptor.url:
            QDesktopServices.openUrl(QUrl(self.descriptor.url))
        super().mouseReleaseEvent(event)

    def minimize(self):
        if self._duration_label:
            self._duration_label.hide()
        if self._location_label:
            self._location_label.hide()
        self.layout().setContentsMargins(10, 4, 10, 4)
        self.setFixedHeight(40)

    def _init_ui(self):
        """Initialize the card UI."""
        self._update_style(hovered=False)
        self.setFixedHeight(100)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Left side: time and duration
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)

        time_label = QLabel(self.descriptor.start_time.strftime('%H:%M'))
        time_label.setFont(QFont("Arial", 14, QFont.Bold))
        time_label.setAlignment(Qt.AlignTop)
        left_layout.addWidget(time_label)

        if self.descriptor.duration:
            self._duration_label = QLabel(f"{self.descriptor.duration:.1f}h")
            self._duration_label.setFont(QFont("Arial", 9))
            self._duration_label.setStyleSheet("color: #888;")
            self._duration_label.setAlignment(Qt.AlignTop)
            left_layout.addWidget(self._duration_label)

        left_layout.addStretch()
        layout.addLayout(left_layout)

        # Right side: summary
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)

        summary_label = QLabel(self.descriptor.summary)
        summary_label.setFont(QFont("Arial", 12, QFont.Bold))
        summary_label.setWordWrap(True)
        right_layout.addWidget(summary_label)

        if self.descriptor.location:
            self._location_label = QLabel(self.descriptor.location)
            self._location_label.setFont(QFont("Arial", 9))
            self._location_label.setStyleSheet("color: #666;")
            self._location_label.setWordWrap(True)
            right_layout.addWidget(self._location_label)

        right_layout.addStretch()
        layout.addLayout(right_layout, 1)

        self.setLayout(layout)
