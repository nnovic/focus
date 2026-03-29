import pytest


def pytest_addoption(parser):
    parser.addoption("--gitlab-token", action="store", default=None, help="GitLab personal access token")


@pytest.fixture
def my_gitlab_token(request):
    return request.config.getoption("--gitlab-token")
