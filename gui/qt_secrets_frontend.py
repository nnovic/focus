import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
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
            import threading
            if threading.current_thread() is threading.main_thread():
                app = QApplication(sys.argv)
        return app


    def prompt_user_to_unlock_safe(self) -> str | None:
        app = self._get_app()
        if app is None:
            print("⚠ Cannot show GUI (not in main thread), skipping this attempt...")
            return None

        dialog = KeyringPasswordDialog()
        # Process events before showing dialog to keep UI responsive
        app.processEvents()
        result = dialog.exec_()
        # Process events again after dialog closes
        app.processEvents()

        if result != QDialog.Accepted:
            print("❌ Unlock cancelled")
            return None

        # User entered keyring password - use it with pexpect
        return dialog.password


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
        # Use done() instead of accept() to avoid potential blocking issues
        self.done(QDialog.Accepted)
