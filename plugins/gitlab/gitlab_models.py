from typing import Any
from datetime import datetime

from core.generic_model_todo_list import GenericModelTodoList
from core.generic_task_descriptor import GenericTaskDescriptor
from core.scm_model_my_pull_requests import ScmModelMyPullRequests
from core.scm_pull_request_descriptor import ScmPullRequestDescriptor


class GitlabTodoDescriptor(GenericTaskDescriptor):
    def __init__(self, todo):
        super().__init__()
        self.__todo = todo

    @property
    def title(self) -> str:
        p = self.__todo.project["name"]
        return f"{p} {self.__todo.state} {self.__todo.target_type}"
    @property
    def description(self) -> str:
        return f"{self.__todo.action_name} {self.__todo.body}"
    @property
    def url(self) -> str | None:
        return self.__todo.target_url

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
    def short_ref(self)->str|None:
        return self.__mr.references["full"]
    
    @property
    def is_ready_to_merge(self) -> bool | None:
        return self.__mr.detailed_merge_status == 'mergeable'
        #return self.__mr.merge_status == 'can_be_merged' and self.__mr.detailed_merge_status == 'mergeable'


    @property
    def has_issues(self) -> bool | None:
        has_open_discussions = self.__mr.blocking_discussions_resolved is False
        is_down_voted = self.__mr.downvotes > 0
        has_conflicts = self.__mr.has_conflicts
        needs_rebase = self.__mr.detailed_merge_status == 'needs_rebase'
        cannot_be_merged = self.__mr.merge_status != 'can_be_merged'
        return has_open_discussions or is_down_voted or has_conflicts or needs_rebase or cannot_be_merged

    @property
    def upvotes(self) -> int:
        return self.__mr.upvotes

    @property
    def created_at(self) -> datetime | None:
        if self.__mr.created_at is None:
            return None
        return datetime.fromisoformat(self.__mr.created_at.replace('Z', ''))


class GitlabModelTodoList(GenericModelTodoList):
    def __init__(self):
        self.__list = []

    @property
    def title(self) -> str:
        return "My Todo list @Gitlab"
    
    def _refresh(self, gl):
        tds = gl.todos.list(
             get_all=True)
        
        new_list = []
        for td in tds:
            desc = GitlabTodoDescriptor(td)
            new_list.append(desc)

        self.__list = new_list


    def _get_tasks(self) -> list[GenericTaskDescriptor]:
        return self.__list



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

    def _get_pull_requests(self) -> list[ScmPullRequestDescriptor]:
        return self.__list
