import os
import xml.etree.ElementTree as ET
import importlib


class FocusConfig:

	def __init__(self):
		self.__configs = {}

	def set_source_config(self, source_id, config):
		self.__configs[source_id]=config

	def get_source_config(self, source_id):
		return self.__configs[source_id]

class FocusSourceConfig:
	def update_from_xml(self, source_node):
		raise NotImplementedError()

def load() -> FocusConfig:
	path = "~/.focus/config.xml"
	path = os.path.expanduser(path) 
	return load_from_file(path)

def load_from_file(config_file: str) -> FocusConfig:

	tree = ET.parse(config_file)
	root = tree.getroot()
	config = FocusConfig()

	__load_sources_from_xml_into_config(root, config)

	return config


def __load_sources_from_xml_into_config(root, config):
	# Load sources
	sources = root.find("config/sources")
	if sources is not None:
		for source in sources.findall("source"):
			__load_source_from_xml_into_config(source, config)

def __load_source_from_xml_into_config(source_node, config):

	source_class_name = source_node.get("class")
	source_id = source_node.get("id")

	# Dynamically import and instantiate the config class
	module_path = f"sources.{source_class_name}.{source_class_name}_config"
	class_name = f"{source_class_name.capitalize()}SourceConfig"

	module = importlib.import_module(module_path)
	config_class = getattr(module, class_name)
	source_config = config_class()
	source_config.update_from_xml(source_node)


	config.set_source_config(source_id, source_config)
