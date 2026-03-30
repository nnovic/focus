from typing import Any


class ScmPullRequestDescriptor:

    @property
    def uuid(self) -> Any:
        raise NotImplementedError()

    @property
    def title(self) -> str:
        return "Untitle merge request"

    @property
    def url(self) -> str | None:
        return None

    @property
    def priority(self) -> int:
        """
        Priorities to ponder:
        - MR that can be merged
        - MR that have open discussions
        - MR that must be rebased
        - MR with downvotes
        - MR getting old
        - MR with no upvotes
        """
        return self.__get_coarse_priority()
    
    def __get_coarse_priority(self) -> int :
        if self.is_ready_to_merge:
            return 90
        if self.has_open_discussions:
            return 80
        return 50
    
    @property
    def is_ready_to_merge(self) -> bool|None:
        return None
    
    @property
    def has_open_discussions(self) -> bool|None:
        return None
    
    
    @property
    def has_open_discussions(self) -> bool|None:
        return None