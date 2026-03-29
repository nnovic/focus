import os
import xml.etree.ElementTree as ET
from sources.gitlab.gitlab_source import GitlabConfig


class FocusConfig:
    def __init__(self):
        self.__load_config()

    def __load_config(self):
        try:
            config_path = os.path.expanduser("~/.focus/config.xml")
            tree = ET.parse(config_path)
            root = tree.getroot()
            self.__load_sources(root)
        except FileNotFoundError:
            pass

    def __load_sources(self, root):
        sources_element = root.find("config/sources")
        if sources_element is not None:
            for source in sources_element:
                if source.tag == "gitlab":
                    GitlabConfig(source)
