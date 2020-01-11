import json
import falcon

from social_network.infrastructure.clock import Clock
from social_network.repositories import users
from social_network.repositories import posts
from social_network.use_cases import create_post
from social_network.use_cases import base


class CreatedPostPresenter(base.OutputBoundary):
    def __init__(self, response: falcon.Response) -> None:
        self.response = response

    def on_success(self, new_post: create_post.Response) -> None:
        self.response.content_type = "application/json"
        self.response.status = falcon.HTTP_201
        self.response.body = json.dumps(
            {"postId": new_post.post_id,
             "userId": new_post.user_id,
             "text": new_post.text,
             "date": str(new_post.created_on.date()),
             "time": str(new_post.created_on.time())})

    def on_failure(self, message: str) -> None:
        self.response.status = falcon.HTTP_400
        self.response.body = message


class Controller(object):
    def __init__(self, post_repository: posts.Repository, user_repository: users.Repository):
        self.post_repository = post_repository
        self.user_repository = user_repository

    def on_post(self, request: falcon.Request, response: falcon.Response, user_id: str) -> None:
        data = json.load(request.bounded_stream)
        use_case = create_post.UseCase(
            self.post_repository, self.user_repository,
            CreatedPostPresenter(response), Clock())
        cp_request = create_post.Request(user_id, data.get("text"))
        use_case.execute(cp_request)
