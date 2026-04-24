from gui.widgets.abstract_card import AbstractCard
from PyQt5.QtWidgets import QFrame

class ConcreteCard(AbstractCard, QFrame):
    def __init__(self):
        QFrame.__init__(self)
        AbstractCard.__init__(self)
    