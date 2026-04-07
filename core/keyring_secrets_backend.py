import sys
import os
import subprocess
import threading
from typing import Optional

try:
    import pexpect
    HAS_PEXPECT = True
except ImportError:
    HAS_PEXPECT = False
    print("Warning: pexpect not installed. Install with: pip install pexpect")

import keyring

# Add parent directory to path so we can import test_keys_gui
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from test_keys_gui import get_password
from core.secrets_manager import *


class KeyringSecretsBackend(SecretsBackend):


    def __init__(self):
        super().__init__()
        self.__keyring_password = None

    def get_secret(self, gui:SecretsFrontend, service_name: str, username: str) -> str:
        """
        Get a secret from the system keyring.

        Keyring is unlocked on first use via __init__.
        """
        try:
            pwd = self.__get_secret(gui, service_name, username)
            if pwd is None:
                raise ValueError(f"No password stored for {service_name}/{username}")
            return pwd
        except Exception as e:
            print(f"\n❌ ERROR: Failed to retrieve secret from keyring")
            print(f"   Service: {service_name}")
            print(f"   Username: {username}")
            print(f"   Error: {type(e).__name__}: {e}")
            raise

    def __get_secret(
        self,gui:SecretsFrontend, service: str, username: str
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
                if self.__keyring_password is None:
                    self.__keyring_password = gui.prompt_user_to_unlock_safe()
                # app = self._get_app()
                if self.__keyring_password is None:
                    continue

                # dialog = KeyringPasswordDialog()
                # if dialog.exec_() != QDialog.Accepted:
                #     print("❌ Unlock cancelled")
                #     return None

                # # User entered keyring password - use it with pexpect
                # keyring_password = dialog.password
                print("🔓 Using password to retrieve from keyring...")

                if HAS_PEXPECT:
                    pwd = self._get_password_with_password(service, username, self.__keyring_password)
                    if pwd:
                        print(f"✓ Retrieved password for {service}/{username}")
                        return pwd
                    else:
                        self.__keyring_password = None
                        print("❌ Password incorrect or retrieval failed")
                else:
                    self.__keyring_password = None
                    print("⚠ pexpect not available, retrying without password...")
                    continue

        self.__keyring_password = None
        print(f"❌ Failed to retrieve password after {max_retries} attempts")
        return None
    
    def _get_password_with_password(self, service: str, username: str, password: str) -> Optional[str]:
        """Get password from keyring using the provided keyring password."""
        try:
            if not HAS_PEXPECT:
                return None

            # Use pexpect to interact with keyring
            script = f"""
import keyring
pwd = keyring.get_password({service!r}, {username!r})
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











# class KeyringSecretsManager(SecretsManager):

#     def __init__(self, ):
#         pass

#     def get_secret(self, service_name: str, username: str) -> str:
#         """
#         Get a secret from the system keyring.

#         Keyring is unlocked on first use via __init__.
#         """
#         try:
#             pwd = get_password(service_name, username)
#             if pwd is None:
#                 raise ValueError(f"No password stored for {service_name}/{username}")
#             return pwd
#         except Exception as e:
#             print(f"\n❌ ERROR: Failed to retrieve secret from keyring")
#             print(f"   Service: {service_name}")
#             print(f"   Username: {username}")
#             print(f"   Error: {type(e).__name__}: {e}")
#             raise
