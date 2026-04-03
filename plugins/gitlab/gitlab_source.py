from typing import Any

from core.data_source import DataSource
import gitlab

from plugins.gitlab.gitlab_models import *

class GitlabSource(DataSource):

    def __init__(self):
        super().__init__()
        self.__gl = None
        self.__my_pull_requests = GitlabModelMyPullRequests()
        self.__my_todo_list = GitlabModelTodoList()
        self.__config = None

    def configure(self, config: Any):
        self.__config = config

    def connect(self) -> None:
        self.__gl = gitlab.Gitlab("https://gitlab.com",
                       private_token=self.__config.token)
        self.__gl.auth()
        
    def disconnect(self) -> None:
        """Close the GitLab connection."""
        if self.__gl is not None:
            self.__gl = None


    def _refresh(self) -> None:
        self.__refresh_my_pull_requests()
        self.__refresh_my_todo_list()


    def __refresh_my_pull_requests(self):
        self.__my_pull_requests._refresh(self.__gl)

    def __refresh_my_todo_list(self):
        self.__my_todo_list._refresh(self.__gl)

    def get_model(self, type: type) -> Any:
        if type is GenericModelTodoList:
            return self.__my_todo_list
        elif type is ScmModelMyPullRequests:
            return self.__my_pull_requests
        else:
            raise NotImplementedError()
