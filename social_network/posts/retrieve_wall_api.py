import json

import falcon

from social_network.infrastructure import base
from social_network.posts import posts
from social_network.posts.use_cases import retrieve_wall
from social_network.users import users


class Presenter(base.OutputBoundary):
    def __init__(self, response: falcon.Response) -> None:
        self.response = response

    def on_success(self, wall_response: retrieve_wall.Response) -> None:
        self.response.content_type = "application/json"
        self.response.status = falcon.HTTP_200
        self.response.body = json.dumps([dict(
            postId=p.id,
            userId=p.user_id,
            text=p.text,
            date=str(p.created_on.date()),
            time=str(p.created_on.time()))
            for p in wall_response.posts])

    def on_failure(self, error: str) -> None:
        self.response.content_type = "text/plain"
        self.response.status = falcon.HTTP_400
        self.response.body = error


class RetrieveWallAPI(object):
    def __init__(self, posts_repository: posts.Repository, users_repository: users.Repository):
        self.posts_repository = posts_repository
        self.users_repository = users_repository

    def on_get(self, request: falcon.Request, response: falcon.Response, user_id: str) -> None:
        use_case = retrieve_wall.UseCase(self.posts_repository, self.users_repository, Presenter(response))
        wall_request = retrieve_wall.Request(user_id=user_id)
        use_case.execute(wall_request)

