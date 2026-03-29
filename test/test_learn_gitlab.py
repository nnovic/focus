import os
from sources.gitlab.gitlab_api import GitlabAPI


def test_lear_gitlab_merge_requests():
	"""Test connecting to GitLab and fetching merge requests"""
	# Get credentials from environment variables
	gitlab_url = os.getenv("GITLAB_URL")
	gitlab_token = os.getenv("GITLAB_TOKEN")
	project_id = os.getenv("GITLAB_PROJECT_ID")

	if not all([gitlab_url, gitlab_token, project_id]):
		print("Skipping test: Set GITLAB_URL, GITLAB_TOKEN, and GITLAB_PROJECT_ID")
		return

	# Connect and fetch
	api = GitlabAPI(gitlab_url, gitlab_token)
	mrs = api.get_merge_requests(project_id)

	# Print results
	print(f"\nFound {len(mrs)} merge requests:")
	for mr in mrs:
		print(f"  - #{mr['id']}: {mr['title']} by {mr['author']} ({mr['state']})")

	assert isinstance(mrs, list)
	assert all("id" in mr for mr in mrs)
