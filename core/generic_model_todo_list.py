from abc import abstractmethod

from core.abstract_model import AbstractModel
from core.generic_task_descriptor import GenericTaskDescriptor
from core.scm_pull_request_descriptor import ScmPullRequestDescriptor


class GenericModelTodoList(AbstractModel):

    @property
    def title(self) -> str:
        return "My todo list"

    @property
    def tasks(self) -> list[GenericTaskDescriptor]:
        pr_list = self._get_tasks()

        return sorted(pr_list, key=lambda pr: pr.priority, reverse=True)
        

    @abstractmethod
    def _get_tasks(self) -> list[GenericTaskDescriptor]:
        raise NotImplementedError()
