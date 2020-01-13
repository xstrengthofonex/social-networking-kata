import json

import falcon

from social_network.users import users
from social_network.users.use_cases import follow


class Presenter(follow.Presenter):
    def __init__(self, response: falcon.Response):
        self.response = response

    def on_success(self):
        self.response.status = falcon.HTTP_201

    def on_failure(self, message: str):
        self.response.status = falcon.HTTP_400
        self.response.content_type = "text/plain"
        self.response.body = message


class FollowUserAPI:
    def __init__(self, user_repository: users.Repository):
        self.user_repository = user_repository
        
    def on_post(self, request: falcon.Request, response: falcon.Response) -> None:
        data = json.load(request.bounded_stream)
        presenter = Presenter(response)
        use_case = follow.UseCase(self.user_repository, presenter)
        follow_request = follow.Request(data.get("followerId"), data.get("followeeId"))
        use_case.execute(follow_request)
