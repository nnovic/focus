from abc import abstractmethod

from core.abstract_model import AbstractModel
from core.scm_pull_request_descriptor import ScmPullRequestDescriptor


class ScmModelMyPullRequests(AbstractModel):

    @property
    def title(self) -> str:
        return "My Pull Requests"

    @property
    def pull_requests(self) -> list[ScmPullRequestDescriptor]:
        pr_list = self._get_pull_requests()

        return sorted(pr_list, key=lambda pr: pr.priority, reverse=True)
        

    @abstractmethod
    def _get_pull_requests(self) -> list[ScmPullRequestDescriptor]:
        raise NotImplementedError()
