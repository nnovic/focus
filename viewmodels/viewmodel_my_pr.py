from models.model_my_pr import ModelMyPR


class ViewModelMyPR:
    def __init__(self, model: ModelMyPR):
        self.title = model.title
        self.pr_names_list = model.pr_names_list
