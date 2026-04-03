#!/usr/bin/env python3
"""
Qt5 GUI for managing keyring passwords with automatic password prompt handling.
"""

import sys
import os
import subprocess
import threading
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

try:
    import pexpect
    HAS_PEXPECT = True
except ImportError:
    HAS_PEXPECT = False
    print("Warning: pexpect not installed. Install with: pip install pexpect")

import keyring


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


class KeyringGUI:
    """Main class for handling keyring operations with Qt5 GUI."""

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

    def _try_unlock_keyring(self):
        """
        Try to unlock keyring by making a test call.
        This will trigger the password prompt if locked.
        """
        try:
            # This will either succeed or trigger a prompt
            keyring.get_password("_test", "_test")
            return True
        except Exception:
            return False

    def _get_password_with_password(self, service: str, username: str, password: str) -> Optional[str]:
        """Get password from keyring using the provided keyring password."""
        try:
            if not HAS_PEXPECT:
                return None

            # Use pexpect to interact with keyring
            script = f"""
import keyring
pwd = keyring.get_password('{service}', '{username}')
print(pwd if pwd else '')
"""
            child = pexpect.spawn(
                f'{sys.executable} -c "{script}"',
                timeout=5,
                encoding='utf-8'
            )

            try:
                # Expect the password prompt
                child.expect("Please enter password for encrypted keyring:")
                child.sendline(password)
                child.expect(pexpect.EOF)
                output = child.before.strip()
                if output and output != "None":
                    return output
                return None
            except pexpect.TIMEOUT:
                return None
            except pexpect.exceptions.EOF:
                output = child.before.strip()
                if output and output != "None":
                    return output
                return None
        except Exception:
            return None

    def get_password_with_gui(
        self, service: str, username: str
    ) -> Optional[str]:
        """
        Retrieve a password from keyring.

        Args:
            service: Service name (e.g., 'gitlab', 'jira')
            username: Username for the service

        Returns:
            The password if found, None otherwise
        """
        max_retries = 3
        for attempt in range(max_retries):
            result = [None]

            def get_in_thread():
                try:
                    pwd = keyring.get_password(service, username)
                    result[0] = pwd
                except Exception as e:
                    result[0] = "ERROR"

            # Run get in a thread with timeout
            thread = threading.Thread(target=get_in_thread, daemon=True)
            thread.start()
            thread.join(timeout=1)  # Wait max 1 second

            if result[0] is not None:
                if result[0] == "ERROR":
                    print(f"❌ Error retrieving password")
                    return None
                elif result[0]:
                    print(f"✓ Retrieved password for {service}/{username}")
                    return result[0]
                else:
                    print(f"❌ No password stored for {service}/{username}")
                    return None

            # If thread is still running, keyring is blocked
            if thread.is_alive():
                attempt_num = attempt + 1
                print(f"\n🔒 Keyring is blocked. Showing GUI popup (attempt {attempt_num}/{max_retries})...")

                app = self._get_app()
                if app is None:
                    print("⚠ Cannot show GUI (not in main thread), skipping this attempt...")
                    continue

                dialog = KeyringPasswordDialog()
                if dialog.exec_() != QDialog.Accepted:
                    print("❌ Unlock cancelled")
                    return None

                # User entered keyring password - use it with pexpect
                keyring_password = dialog.password
                print("🔓 Using password to retrieve from keyring...")

                if HAS_PEXPECT:
                    pwd = self._get_password_with_password(service, username, keyring_password)
                    if pwd:
                        print(f"✓ Retrieved password for {service}/{username}")
                        return pwd
                    else:
                        print("❌ Password incorrect or retrieval failed")
                else:
                    print("⚠ pexpect not available, retrying without password...")
                    continue

        print(f"❌ Failed to retrieve password after {max_retries} attempts")
        return None

    def store_password_with_gui(
        self, service: str, username: str, password: str
    ) -> bool:
        """
        Store a password in keyring.

        Assumes keyring is already unlocked (via ensure_keyring_unlocked).

        Args:
            service: Service name
            username: Username
            password: Password to store

        Returns:
            True if successful
        """
        import threading

        max_retries = 3
        for attempt in range(max_retries):
            result = [None]

            def store_in_thread():
                try:
                    keyring.set_password(service, username, password)
                    result[0] = True
                except Exception as e:
                    result[0] = False

            # Run store in a thread with timeout
            thread = threading.Thread(target=store_in_thread, daemon=True)
            thread.start()
            thread.join(timeout=1)  # Wait max 1 second

            if result[0] is True:
                print(f"✓ Password stored for {service}/{username}")
                return True

            # If thread is still running, keyring is blocked
            if thread.is_alive():
                attempt_num = attempt + 1
                print(f"\n🔒 Keyring is blocked. Showing GUI popup (attempt {attempt_num}/{max_retries})...")

                app = self._get_app()
                if app is None:
                    print("⚠ Cannot show GUI (not in main thread), skipping this attempt...")
                    continue

                dialog = KeyringPasswordDialog()
                if dialog.exec_() != QDialog.Accepted:
                    print("❌ Store cancelled")
                    return False

                print("🔓 Retrying store...")
                continue
            else:
                # Thread finished but returned False
                print(f"❌ Error storing password")
                return False

        print(f"❌ Failed to store password after {max_retries} attempts")
        return False


# Global instance for easy access
_gui_instance = None


def get_keyring_gui():
    """Get the global KeyringGUI instance."""
    global _gui_instance
    if _gui_instance is None:
        _gui_instance = KeyringGUI()
    return _gui_instance


def get_password(service: str, username: str) -> Optional[str]:
    """Convenience function to get password (assumes keyring is unlocked)."""
    return get_keyring_gui().get_password_with_gui(service, username)


def store_password(service: str, username: str, password: str) -> bool:
    """Convenience function to store password (assumes keyring is unlocked)."""
    return get_keyring_gui().store_password_with_gui(service, username, password)


if __name__ == "__main__":
    gui = KeyringGUI()

    print("=" * 60)
    print("Keyring GUI Test")
    print("=" * 60)

    # IMPORTANT: Unlock keyring first!
    print("\n0. Unlocking keyring...")
    if not gui.ensure_keyring_unlocked():
        print("Cannot proceed without keyring")
        sys.exit(1)

    # Retrieve GitLab credentials
    print("\n1. Retrieving GitLab credentials...")
    gitlab_pwd = gui.get_password_with_gui("focus_GitlabSource__https://gitlab.com", "avincon.groupe-atlantic.com")
    if gitlab_pwd:
        print(f"✓ GitLab password: {gitlab_pwd[:20]}..." if len(gitlab_pwd) > 20 else f"✓ GitLab password: {gitlab_pwd}")
    else:
        print("❌ No GitLab password found")
