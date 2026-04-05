from abc import abstractmethod
from typing import Any
import threading


class SecretsFrontend:
    
    @abstractmethod
    def prompt_user_to_unlock_safe(self) -> str | None:
        raise NotImplementedError()

class SecretsBackend:

    @abstractmethod
    def get_secret(self,  gui:SecretsFrontend, service_name: str, username: str) -> str:
        raise NotImplementedError()


class SecretsManager:

    def __init__(self):
        self.__lock = threading.Lock()

    def set_backend(self, back:SecretsBackend):
        self.__backend = back

    def set_frontend(self, front :SecretsFrontend):
        self.__frontend = front

    def get_secret(self, service_name: str, username: str) -> str | None:
        with self.__lock:
            return self.__backend.get_secret(self.__frontend, service_name, username)


secrets_manager = SecretsManager()
