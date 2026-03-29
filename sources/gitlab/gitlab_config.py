class GitlabConfig:
    def __init__(self, element=None):
        self.personal_access_token = None
        if element is not None:
            self.__load_from_xml(element)

    def __load_from_xml(self, element):
        credentials = element.find("credentials")
        if credentials is not None:
            self.personal_access_token = credentials.get("token")
