import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QTimer, QEventLoop
from core.secrets_manager import SecretsFrontend


class QtSecretsFrontend(SecretsFrontend):
    def __init__(self):
        self.app = self._get_app()
        self._keyring_unlocked = False

    def _get_app(self):
        """Get or create the QApplication instance."""
        app = QApplication.instance()
        if app is None:
            # Only create QApplication in the main thread
            if threading.current_thread() is threading.main_thread():
                app = QApplication(sys.argv)
        return app

    def prompt_user_to_unlock_safe(self) -> str | None:
        app = self._get_app()
        if app is None:
            print("⚠ Cannot show GUI (not in main thread), skipping this attempt...")
            return None

        # If we're on the main thread, show dialog directly
        if threading.current_thread() is threading.main_thread():
            dialog = KeyringPasswordDialog()
            result = dialog.exec_()
            if result != QDialog.Accepted:
                print("❌ Unlock cancelled")
                return None
            return dialog.password

        # If we're on a background thread, use a local event loop to wait for dialog
        password_result = [None]
        dialog_holder = [None]
        event_loop = QEventLoop()

        def show_dialog_on_main_thread():
            dialog = KeyringPasswordDialog()
            dialog_holder[0] = dialog
            result = dialog.exec_()
            if result == QDialog.Accepted:
                password_result[0] = dialog.password
            else:
                print("❌ Unlock cancelled")
            event_loop.quit()

        # Schedule dialog show on main thread
        QTimer.singleShot(0, show_dialog_on_main_thread)

        # Run local event loop to process main thread events
        event_loop.exec_()

        return password_result[0]


class KeyringPasswordDialog(QDialog):
    """Dialog to prompt for keyring password."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.password = None
        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("Keyring Password Required")
        self.setModal(True)
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Info label
        info_label = QLabel("Your keyring is locked.\nPlease enter your keyring password to continue:")
        layout.addWidget(info_label)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter keyring password")
        self.password_input.returnPressed.connect(self.unlock_keyring)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QVBoxLayout()

        unlock_btn = QPushButton("Unlock")
        unlock_btn.clicked.connect(self.unlock_keyring)
        button_layout.addWidget(unlock_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Focus on password input
        self.password_input.setFocus()

    def unlock_keyring(self):
        """Unlock keyring with entered password."""
        self.password = self.password_input.text()
        if not self.password:
            QMessageBox.warning(self, "Error", "Password cannot be empty")
            return
        self.accept()
