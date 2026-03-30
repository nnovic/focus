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
