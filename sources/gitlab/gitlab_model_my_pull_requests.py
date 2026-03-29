from models.model_my_pull_requests import ModelMyPullRequests
from .gitlab_api import GitlabAPI


class GitlabModelMyPullRequests(ModelMyPullRequests):
	def __init__(self, url: str = None, private_token: str = None, project_id: str = None):
		super().__init__()
		self.title = "my pull requests"
		self.merge_requests = []
		self.url = url
		self.private_token = private_token
		self.project_id = project_id

	def fetch_merge_requests(self):
		"""Fetch merge requests from GitLab"""
		if not all([self.url, self.private_token, self.project_id]):
			raise ValueError("url, private_token, and project_id must be set")

		api = GitlabAPI(self.url, self.private_token)
		self.merge_requests = api.get_merge_requests(self.project_id)