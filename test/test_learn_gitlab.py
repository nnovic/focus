
from sources.gitlab.gitlab_source import GitlabSource

# api
# api-read



def test_gitlab_source():

    source = GitlabSource()
    source.connect()
    source.refresh()

    model = source.get_model(type="ScmModelMyPullRequests")
    
    print (model.title)
    print (model.priority)
    
    for mr_desc in model.pull_requests:
        print (mr_desc.title)
