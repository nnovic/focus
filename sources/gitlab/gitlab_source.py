import gitlab
from models.model_my_pr import ModelMyPR
from sources.data_source import DataSource
from sources.gitlab.gitlab_config import GitlabConfig
from sources.gitlab.gitlab_model_my_pr import GitlabModelMyPR


class GitlabSource(DataSource):
    def __init__(self, config: GitlabConfig):
        self._config = config
        self._gl: gitlab.Gitlab | None = None

    def connect(self) -> None:
        self.__connect_with_personal_access_token()
        self.__get_data()

    def disconnect(self) -> None:
        self._gl = None

    def __connect_with_personal_access_token(self) -> None:
        self._gl = gitlab.Gitlab("https://gitlab.com", private_token=self._config.personal_access_token)

    def __get_data(self) -> None:
        self._gl.mergerequests.list(per_page=1)

    def get_model_my_pr(self) -> ModelMyPR:
        return GitlabModelMyPR()
