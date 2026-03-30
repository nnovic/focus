
from core import focus_config


class FocusApp:

    def __init__(self):
        self.__load_config()

    def __load_config(self):
        self.__config = focus_config.load()

    @property
    def config(self) -> focus_config.FocusConfig:
        return self.__config
