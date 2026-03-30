from abc import abstractmethod

from models.model_my_pull_requests import ModelMyPullRequests


class AbstractView:
	@abstractmethod
	def refresh(self, model: ModelMyPullRequests):
		pass