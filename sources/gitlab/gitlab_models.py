from typing import Any

from core.scm_model_my_pull_requests import ScmModelMyPullRequests
from core.scm_pull_request_descriptor import ScmPullRequestDescriptor

class GitlabPullRequestDescriptor(ScmPullRequestDescriptor):

    def __init__(self, merge_request):
        super().__init__()
        self.__mr = merge_request

    @property
    def uuid(self) -> Any:
        return self.__mr.id

    @property
    def title(self) -> str:
        return self.__mr.title

    @property
    def url(self) -> str | None:
        return self.__mr.web_url

    @property
    def is_ready_to_merge(self) -> bool|None:
        return self.__mr.merge_status == 'can_be_merged'
    
    @property
    def has_open_discussions(self) -> bool|None:
        return self.__mr.blocking_discussions_resolved is False
    
    # def has_no_upvotes
    

class GitlabModelMyPullRequests(ScmModelMyPullRequests):

    def __init__(self):
        self.__list = []

    @property
    def title(self) -> str:
        return "My Pull Requests @Gitlab"

    def _refresh(self, gl):
        mrs = gl.mergerequests.list(
            author_id=gl.user.id, state="opened", get_all=True)
        
        new_list = []
        for mr in mrs:
            desc = GitlabPullRequestDescriptor(mr)
            new_list.append(desc)

        self.__list = new_list
        
    @property
    def pull_requests(self) -> list[ScmPullRequestDescriptor]:
        return self.__list
    