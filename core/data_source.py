from typing import Any


class DataSource:

    def connect(self) -> None:
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()

    def refresh(self) -> None:
        raise NotImplementedError()

    def get_model(self, type_hint: str) -> Any:
        raise NotImplementedError()
