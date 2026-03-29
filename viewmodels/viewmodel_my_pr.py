class ViewModelMyPR:
    def __init__(self, title: str = "gitlab", pr_names_list: list[str] = ["mr1", "mr2"]):
        self.title = title
        self.pr_names_list = pr_names_list
