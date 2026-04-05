import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from core.focus_app import FocusApp
from core.keyring_secrets_backend import KeyringSecretsBackend
from gui.qt_secrets_frontend import QtSecretsFrontend
from gui import MainWindow


def main():
    focus_app = FocusApp()
    qapp = QApplication(sys.argv)
    window = MainWindow(focus_app)

    from core import secrets_manager as sm_module
    sm_module.secrets_manager.set_backend( KeyringSecretsBackend() )
    sm_module.secrets_manager.set_frontend(QtSecretsFrontend())

    window.show()

    # Start focus_app in the background after the event loop is running
    QTimer.singleShot(0, focus_app.start)

    sys.exit(qapp.exec_())


if __name__ == "__main__":
    main()
