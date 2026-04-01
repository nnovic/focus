from PyQt5.QtWidgets import QLayout
from PyQt5.QtCore import Qt, QSize, QPoint


class FlowLayout(QLayout):
    """A layout that arranges widgets like Java's FlowLayout."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []

    def addItem(self, item):
        self.items.append(item)

    def itemAt(self, index):
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def count(self):
        return len(self.items)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QPoint(0, 0), width, True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect.topLeft(), rect.width(), False)

    def sizeHint(self):
        size = self.minimumSize()
        return size

    def minimumSize(self):
        size = QSize()
        for item in self.items:
            widget = item.widget()
            if widget:
                size = size.expandedTo(widget.minimumSizeHint())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def doLayout(self, position, width, test_only):
        x = position.x() + self.contentsMargins().left()
        y = position.y() + self.contentsMargins().top()
        line_height = 0
        max_y = y

        for item in self.items:
            widget = item.widget()
            if not widget:
                continue

            space_x = self.spacing()
            space_y = self.spacing()
            next_x = x + item.sizeHint().width() + space_x

            # Check if we need to wrap to next line
            if next_x - space_x > position.x() + width - self.contentsMargins().right() and line_height > 0:
                x = position.x() + self.contentsMargins().left()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                widget.setGeometry(x, y, item.sizeHint().width(), item.sizeHint().height())

            x = next_x
            line_height = max(line_height, item.sizeHint().height())
            max_y = max(max_y, y + line_height)

        return max_y - position.y() + self.contentsMargins().bottom()
