import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from focus_app import FocusApp


def main():
    focus_app = FocusApp()
    app = QApplication(sys.argv)

    window = MainWindow(focus_app)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
