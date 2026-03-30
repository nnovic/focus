class AbstractModel:

    @property
    def title(self) -> str:
        return "Untitled"

    @property
    def priority(self) -> int:
        return 50
