from typing import Any

# from core.secrets_manager import secrets_manager
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

    @property
    def __server(self):
        try:
            return self.__config.server
        except KeyError:
            return "https://gitlab.com"

    # @property
    # def __username(self):
    #     return self.__config.username

    # @property
    # def __service_name(self):
    #     return self.decorate(self.__server)

    def _connect(self) -> None:
        try:
            # token = secrets_manager.get_secret(
            #     self.__service_name, self.__username)
            self.__gl = gitlab.Gitlab(self.__server,
                                      private_token=self.__config.token)
            self.__gl.auth()
        except gitlab.GitlabAuthenticationError as e:
            breakpoint()
            if e.response_code == 401:
                raise ConnectionRefusedError(e.args)
            raise ConnectionAbortedError(e.args)
        except Exception as e:
            breakpoint()
            raise ConnectionAbortedError(e.args)

    def _disconnect(self) -> None:
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
