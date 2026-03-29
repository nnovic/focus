import gitlab


class GitlabAPI:
    def __init__(self, url: str, private_token: str):
        """
        Initialize GitLab API client.

        Args:
            url: GitLab instance URL (e.g., "https://gitlab.com")
            private_token: Personal access token for authentication
        """
        self.gl = gitlab.Gitlab(url, private_token=private_token)
        self.gl.auth()

    def get_merge_requests(self, project_id: str | int, state: str = "opened") -> list:
        """
        Get merge requests for a project.

        Args:
            project_id: GitLab project ID or path
            state: State of MRs to fetch ("opened", "closed", "merged", "all")

        Returns:
            List of merge requests with relevant details
        """
        project = self.gl.projects.get(project_id)
        mrs = project.mergerequests.list(state=state, get_all=True)

        return [
            {
                "id": mr.iid,
                "title": mr.title,
                "author": mr.author["name"],
                "state": mr.state,
                "web_url": mr.web_url,
            }
            for mr in mrs
        ]
