from abc import ABC, abstractmethod
from models.model_my_pr import ModelMyPR


class DataSource(ABC):
    @abstractmethod
    def get_model_my_pr(self) -> ModelMyPR:
        pass
