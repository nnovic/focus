from models.model_my_pr import ModelMyPR
from sources.data_source import DataSource
from sources.gitlab.gitlab_model_my_pr import GitlabModelMyPR


class GitlabSource(DataSource):
    def get_model_my_pr(self) -> ModelMyPR:
        return GitlabModelMyPR()
