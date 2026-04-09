from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTime

from core.calendar_event_descriptor import CalendarEventDescriptor


class CalendarEventCard(QFrame):
    def __init__(self, descriptor: CalendarEventDescriptor):
        super().__init__()
        self.descriptor = descriptor
        self._bg_color = "#f5f5f5"
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

    def _init_ui(self):
        """Initialize the card UI."""
        self._update_style(hovered=False)
        self.setFixedHeight(100)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Left side: time
        time_label = QLabel(self.descriptor.start_time.strftime('%H:%M'))
        time_label.setFont(QFont("Arial", 14, QFont.Bold))
        time_label.setAlignment(Qt.AlignTop)
        layout.addWidget(time_label)

        # Right side: summary and duration
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)

        summary_label = QLabel(self.descriptor.summary)
        summary_label.setFont(QFont("Arial", 12, QFont.Bold))
        summary_label.setWordWrap(True)
        right_layout.addWidget(summary_label)

        # Duration label if available
        if self.descriptor.duration:
            duration_label = QLabel(f"Duration: {self.descriptor.duration:.1f} hours")
            duration_label.setFont(QFont("Arial", 9))
            duration_label.setStyleSheet("color: #888;")
            right_layout.addWidget(duration_label)

        right_layout.addStretch()
        layout.addLayout(right_layout, 1)

        self.setLayout(layout)
