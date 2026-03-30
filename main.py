import sys
from PyQt5.QtWidgets import QApplication

from core.focus_app import FocusApp
from gui import MainWindow


def main():
    focus_app = FocusApp()
    
    qapp = QApplication(sys.argv)
    window = MainWindow(focus_app)
    window.show()
    sys.exit(qapp.exec_())


if __name__ == "__main__":
    main()
