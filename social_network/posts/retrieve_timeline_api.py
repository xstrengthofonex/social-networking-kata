import json

import falcon

from social_network.infrastructure import base
from social_network.posts import posts
from social_network.posts.use_cases import retrieve_timeline
from social_network.users import users


class Presenter(base.OutputBoundary):
    def __init__(self, response: falcon.Response) -> None:
        self.response = response

    def on_success(self, timeline_response: retrieve_timeline.Response) -> None:
        self.response.content_type = "application/json"
        self.response.status = falcon.HTTP_200
        self.response.body = json.dumps([
            dict(userId=p.user_id,
                 postId=p.id,
                 text=p.text,
                 date=str(p.created_on.date()),
                 time=str(p.created_on.time()))
            for p in timeline_response.posts])

    def on_failure(self, error: str) -> None:
        self.response.content_type = "text/plain"
        self.response.status = falcon.HTTP_400
        self.response.body = error


class RetrieveTimelineAPI(object):
    def __init__(self, post_repository: posts.Repository, user_repository: users.Repository):
        self.post_repository = post_repository
        self.user_repository = user_repository

    def on_get(self, request: falcon.Request, response: falcon.Response, user_id: str) -> None:
        use_case = retrieve_timeline.UseCase(
            self.post_repository, self.user_repository, Presenter(response))
        rt_request = retrieve_timeline.Request(user_id=user_id)
        use_case.execute(rt_request)
