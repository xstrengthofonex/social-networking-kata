import json

import falcon

from social_network.repositories import posts, users
from social_network.use_cases import retrieve_timeline, base


class TimelinePresenter(base.OutputBoundary):
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
            for p in reversed(timeline_response.posts)])

    def on_failure(self, error: str) -> None:
        pass


class Controller(object):
    def __init__(self, post_repository: posts.Repository, user_repository: users.Repository):
        self.post_repository = post_repository
        self.user_repository = user_repository

    def on_get(self, request: falcon.Request, response: falcon.Response, user_id: str) -> None:
        use_case = retrieve_timeline.UseCase(
            self.post_repository, self.user_repository, TimelinePresenter(response))
        rt_request = retrieve_timeline.Request(user_id=user_id)
        use_case.execute(rt_request)
