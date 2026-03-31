
from PyQt5.QtWidgets import QWidget
from gui.views.abstract_view import AbstractView


class ConcreteView(AbstractView, QWidget):
    def __init__(self):
        QWidget.__init__(self)
        AbstractView.__init__(self)

