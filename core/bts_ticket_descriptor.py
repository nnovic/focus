from typing import Any, Final
from datetime import datetime


class BtsTicketPriority:
#     READY_TO_MERGE_AND_UPVOTED: Final[int] = 90
#     READY_TO_MERGE: Final[int] = 80
#     IS_UPVOTED: Final[int] = 70
    IN_PROGRESS: Final[int] = 70
    TO_DO: Final[int] = 50
    BLOCKED: Final[int] = 30
    DONE: Final[int] = 10


class BtsTicketDescriptor:

    # @property
    # def days_old(self) -> int | None:
    #     if self.created_at is None:
    #         return None
    #     delta = datetime.now() - self.created_at
    #     return delta.days
    
    @property
    def created_at(self) -> datetime | None:
        return None

    @property
    def uuid(self) -> Any:
        raise NotImplementedError()

    @property
    def title(self) -> str:
        return "Untitle ticket"

    @property
    def url(self) -> str | None:
        return None

    @property
    def is_done(self) -> bool:
        return False
    
    @property
    def is_blocked(self):
        return False
    
    @property
    def is_in_progress(self):
        return False

    @property
    def priority(self) -> int:
    #     """
    #     Priorities to ponder:
    #     - MR that can be merged
    #     - MR that have open discussions
    #     - MR that must be rebased
    #     - MR with downvotes
    #     - MR getting old
    #     - MR with no upvotes
    #     """
        prio = _evaluate_base_priority(self)
        if prio < 0:
            prio = 0
        if prio > 100:
            prio = 100
        return prio

    # @property
    # def is_ready_to_merge(self) -> bool | None:
    #     return None

    # @property
    # def has_issues(self) -> bool | None:
    #     return None

    # @property
    # def upvotes(self) -> int:
    #     return -1

    
def _evaluate_base_priority(desc: BtsTicketDescriptor) -> int:
    prio = 0
    if desc.is_done:
        prio = BtsTicketPriority.DONE
    if desc.is_blocked:
        prio = BtsTicketPriority.BLOCKED
    elif desc.is_in_progress:
        prio = BtsTicketPriority.IN_PROGRESS
#     elif desc.is_ready_to_merge:
#         if desc.upvotes > 0:
#             prio = ScmPullRequestPriority.READY_TO_MERGE_AND_UPVOTED
#         else:
#             prio = ScmPullRequestPriority.READY_TO_MERGE
#     elif desc.upvotes > 0:
#         prio = ScmPullRequestPriority.IS_UPVOTED
    else:
        prio = BtsTicketPriority.TO_DO
#     prio += __fine_tune_priority_by_age(desc)
    return prio


# def __fine_tune_priority_by_age(desc: ScmPullRequestDescriptor) -> int:
#     age = desc.days_old
#     if age is None or age < 0:
#         return 0
#     elif age >= 10:
#         return 9
#     else:
#         return age

# def __is_too_old(desc: ScmPullRequestDescriptor) -> bool:
#     if desc.days_old is None:
#         return False
#     return desc.days_old > 30

