import os
import xml.etree.ElementTree as ET
import importlib


class FocusConfig:

    def __init__(self):
        self.sources = {}
        self.views = {}

    def set_source_config(self, source_id, config):
        self.sources[source_id] = config

    def get_source_config(self, source_id):
        return self.sources[source_id]

    def set_view_config(self, view_id, config):
        self.views[view_id] = config

    def get_view_config(self, view_id):
        return self.views[view_id]


class GenericConfig:
    def __init__(self):
        self.__params = {}

    def update_from_xml(self, source_node):
        params_list = source_node.findall("param")
        for param_node in params_list:
            param_name = param_node.get("name")
            param_value = param_node.text
            self.__params[param_name] = param_value

    def __getattr__(self, name):
        return self.__params[name]


class SourceConfig(GenericConfig):

    def __init__(self):
        super().__init__()
        self.__plugin = None

    def update_from_xml(self, source_node):
        self.__plugin = source_node.get("plugin")
        super().update_from_xml(source_node)

    @property
    def plugin(self) -> str:
        return self.__plugin

    # def _update_from_xml(self, source_node):
    #     raise NotImplementedError()


class ViewConfig(GenericConfig):

    def __init__(self):
        super().__init__()
        self.__class_name = None
        self.__source_id = None

    def update_from_xml(self, view_node):
        self.__class_name = view_node.get("class")
        self.__source_id = view_node.get("source_id")
        super().update_from_xml(view_node)

    @property
    def class_name(self) -> str:
        return self.__class_name
    
    @property
    def source_id(self) -> str:
        return self.__source_id


def load() -> FocusConfig:
    path = "~/.focus/config.xml"
    path = os.path.expanduser(path)
    return load_from_file(path)


def load_from_file(config_file: str) -> FocusConfig:

    tree = ET.parse(config_file)
    root = tree.getroot()
    config = FocusConfig()

    __load_sources_from_xml_into_config(root, config)
    __load_views_from_xml_into_config(root, config)

    return config


def __load_sources_from_xml_into_config(root, config):
    # Load sources
    sources = root.find("config/sources")
    if sources is not None:
        for source in sources.findall("source"):
            __load_source_from_xml_into_config(source, config)


def __load_source_from_xml_into_config(source_node, config):

    source_config = SourceConfig()
    source_config.update_from_xml(source_node)

    # plugin_name = source_node.get("plugin")
    source_id = source_node.get("id")

    # Dynamically import and instantiate the config class
    # module_path = f"plugins.{plugin_name}.{plugin_name}_config"
    # class_name = f"{plugin_name.capitalize()}SourceConfig"

    # module = importlib.import_module(module_path)
    # config_class = getattr(module, class_name)
    # source_config = config_class()
    # source_config.update_from_xml(source_node)

    config.set_source_config(source_id, source_config)


def __load_views_from_xml_into_config(root, config):
    # Load sources
    views = root.find("config/views")
    if views is not None:
        for view in views.findall("view"):
            __load_view_from_xml_into_config(view, config)


def __load_view_from_xml_into_config(view_node, config):
    view_config = ViewConfig()
    view_config.update_from_xml(view_node)

    view_id = view_node.get("id")


    config.set_view_config(view_id, view_config)