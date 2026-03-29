import pytest
from sources.gitlab.gitlab_config import GitlabConfig
from sources.gitlab.gitlab_source import GitlabSource


def test_connect_fails_if_no_credientials():
    source = GitlabSource(config=GitlabConfig())
    with pytest.raises(Exception):
        source.connect()


def test_connect_success(my_gitlab_token):
    config = GitlabConfig()
    config.personal_access_token = my_gitlab_token
    source = GitlabSource(config=config)
    source.connect()
    source.disconnect()
