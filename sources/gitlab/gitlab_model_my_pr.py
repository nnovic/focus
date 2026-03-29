from models.model_my_pr import ModelMyPR


class GitlabModelMyPR(ModelMyPR):
    def __init__(self):
        super().__init__(title="gitlab", pr_names_list=["mr1", "mr2"])
