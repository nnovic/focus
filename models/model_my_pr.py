class ModelMyPR:
    def __init__(self, title: str = "gitlab", pr_names_list: list[str] = None):
        self.title = title
        self.pr_names_list = pr_names_list if pr_names_list is not None else []
