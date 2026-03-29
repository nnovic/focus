from abc import ABC, abstractmethod
from models.model_my_pr import ModelMyPR


class DataSource(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def get_model_my_pr(self) -> ModelMyPR:
        pass
