from typing import Any


class AbstractView:
    """Base class for all views in the application."""


    def init__(self, ):
        self.__source_id = None


    @property
    def source_id(self) -> Any:
        return self.__source_id

    @source_id.setter
    def source_id(self, value: Any) -> None:
        self.__source_id = value
        
    @property
    def best_models(self) -> list[type]:
        """Return a list of model classes that this view can display."""
        raise NotImplementedError()

    def refresh(self, model):
        """Refresh the view with new model data."""
        raise NotImplementedError()
