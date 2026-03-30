from core.focus_config import FocusSourceConfig


class GitlabSourceConfig(FocusSourceConfig):
	
	def __init__(self):
		super().__init__()
		self.__reset_credentials()

	def __reset_credentials(self):
		self.__token = None


	def update_from_xml(self, source_node):
		self.__update_credentials(source_node)

	def __update_credentials(self, source_node):
		self.__reset_credentials()
		credentials = source_node.find('credentials')
		if credentials is not None:
			token = credentials.get('token')
			if token is not None:
				self.__token = token

	@property
	def personal_access_token(self) -> str:
		return self.__token
	