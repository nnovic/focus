class AbstractView:
    """Base class for all views in the application."""

    @property
    def best_models(self) -> list[type]:
        """Return a list of model classes that this view can display."""
        raise NotImplementedError()

    def refresh(self, model):
        """Refresh the view with new model data."""
        raise NotImplementedError()
