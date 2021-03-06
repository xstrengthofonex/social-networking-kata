import json

import falcon

from social_network.common import boundary
from social_network.users import users
from social_network.users.use_cases import register_user


class Presenter(boundary.Output):
    def __init__(self, response: falcon.Response) -> None:
        self.response = response

    def on_success(self, new_user: register_user.Response) -> None:
        self.response.content_type = "application/json"
        self.response.status = falcon.HTTP_201
        self.response.body = json.dumps(
            {"userId": new_user.user_id,
             "username": new_user.username,
             "about": new_user.about})

    def on_failure(self, message: str) -> None:
        self.response.status = falcon.HTTP_400
        self.response.body = message


class RegisterUserAPI(object):
    def __init__(self, user_repository: users.Repository):
        self.user_repository = user_repository

    def on_post(self, request: falcon.Request, response: falcon.Response) -> None:
        data = json.load(request.bounded_stream)
        use_case = register_user.UseCase(self.user_repository, Presenter(response))
        ru_request = register_user.Request(data.get("username"), data.get("password"), data.get("about"))
        use_case.execute(ru_request)
