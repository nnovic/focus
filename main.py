import sys
from PyQt5.QtWidgets import QApplication

from core.focus_app import FocusApp
from core.keyring_secrets_backend import KeyringSecretsBackend
from gui.qt_secrets_frontend import QtSecretsFrontend
from gui import MainWindow


def main():
    from core import secrets_manager as sm_module
    #sm_module.secrets_manager = KeyringSecretsManager()
    sm_module.secrets_manager.set_backend( KeyringSecretsBackend() )
    sm_module.secrets_manager.set_frontend(QtSecretsFrontend())
    
    qapp = QApplication(sys.argv)
    focus_app = FocusApp()
    focus_app.start()
    window = MainWindow(focus_app)
    window.show()
    sys.exit(qapp.exec_())


if __name__ == "__main__":
    main()
