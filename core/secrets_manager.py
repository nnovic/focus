from abc import abstractmethod
from typing import Any


class SecretsManager:

    @abstractmethod
    def get_secret(self, service_name: Any, username: Any) -> Any:
        raise NotImplementedError()


secrets_manager = None
