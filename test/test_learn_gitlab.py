
from core import focus_config
from sources.gitlab.gitlab_source import GitlabSource

# api
# api-read


def test_gitlab_source():

    global_cfg = focus_config.load()
    gitlab_cfg = global_cfg.get_source_config("1")

    source = GitlabSource()
    source.configure(gitlab_cfg)
    source.connect()
    source.refresh()

    model = source.get_model(type="ScmModelMyPullRequests")
    
    print (model.title)
    print (model.priority)
    
    for mr_desc in model.pull_requests:
        print (str(mr_desc.priority) + " --- " + mr_desc.title)
        
