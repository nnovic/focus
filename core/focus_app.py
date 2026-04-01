
import importlib

from core import focus_config
from core.data_source import DataSource


class FocusApp:

    def __init__(self):
        self.__sources = {}
        self.__load_config()
        self.__create_sources()

    def __load_config(self):
        self.__config = focus_config.load()

    def __create_sources(self):
        for id in self.__config.sources:
            config = self.__config.get_source_config(id)
            source_plugin_name = config.plugin

            # Dynamically import and instantiate the config class
            module_path = f"plugins.{source_plugin_name}.{source_plugin_name}_source"
            class_name = f"{source_plugin_name.capitalize()}Source"

            module = importlib.import_module(module_path)
            source_class = getattr(module, class_name)
            source = source_class()
            source.configure(config)

            self.__register_source(id, source)

    def __register_source(self, id, source):
        self.__sources[id] = source
        source.on_refresh(lambda: self.__on_source_refresh(id))

    def __on_source_refresh(self, source_id):
        pass

    @property
    def config(self) -> focus_config.FocusConfig:
        return self.__config

    def get_source(self, source_id):
        return self.__sources[source_id]
    
    @property
    def sources(self) -> list[str]:
        return list(self.__sources.keys())

    def start(self):
        for id in self.__sources:
            source = self.__sources[id]
            source.start()
