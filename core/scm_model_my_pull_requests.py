from core.abstract_model import AbstractModel
from core.scm_pull_request_descriptor import ScmPullRequestDescriptor


class ScmModelMyPullRequests(AbstractModel):


    @property
    def title(self) -> str:
        return "My Pull Requests"

    @property
    def pull_requests(self) -> list[ScmPullRequestDescriptor]:
        raise NotImplementedError()