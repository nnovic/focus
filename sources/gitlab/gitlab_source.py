from typing import Any

from core.data_source import DataSource
import gitlab

from sources.gitlab.gitlab_models import GitlabModelMyPullRequests

class GitlabSource(DataSource):

    def __init__(self):
        self.__gl = None
        self.__my_pull_requests = GitlabModelMyPullRequests()

    def connect(self) -> None:
        self.__gl = gitlab.Gitlab("https://gitlab.com",
                       private_token="glpat-yYaYNc66ImFGHV-RJbt3bGM6MQpvOjEKdTo0b2Niag8.01.170oeoqsw")
        self.__gl.auth()
    

    def refresh(self) -> None:
        self.__refresh_my_pull_requests()


    def __refresh_my_pull_requests(self):
        # Fetch all merge requests created by this user
        self.__my_pull_requests._refresh(self.__gl)

    def get_model(self, type: str) -> Any:
        return self.__my_pull_requests
