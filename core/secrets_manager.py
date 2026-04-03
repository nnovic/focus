from abc import abstractmethod
from typing import Any
import sys
import os

# Add parent directory to path so we can import test_keys_gui
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_keys_gui import get_password


class SecretsManager:

    @abstractmethod
    def get_secret(self, service_name: Any, username: Any) -> Any:
        raise NotImplementedError()


class KeyringSecretsManager(SecretsManager):

    def __init__(self):
        pass

    def get_secret(self, service_name: str, username: str) -> str:
        """
        Get a secret from the system keyring.

        Keyring is unlocked on first use via __init__.
        """
        try:
            pwd = get_password(service_name, username)
            if pwd is None:
                raise ValueError(f"No password stored for {service_name}/{username}")
            return pwd
        except Exception as e:
            print(f"\n❌ ERROR: Failed to retrieve secret from keyring")
            print(f"   Service: {service_name}")
            print(f"   Username: {username}")
            print(f"   Error: {type(e).__name__}: {e}")
            raise


secrets_manager = KeyringSecretsManager()
