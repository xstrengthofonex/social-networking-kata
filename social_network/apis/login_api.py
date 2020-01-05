import json

import falcon

from social_network.repositories import users
from social_network.use_cases import login, base


class Presenter(base.OutputBoundary):
    def __init__(self, response:falcon.Response) -> None:
        self.response = response

    def on_success(self, logged_in_user: login.Response) -> None:
        self.response.content_type = "application/json"
        self.response.status = falcon.HTTP_OK
        self.response.body = json.dumps(
            {"userId": logged_in_user.user_id,
             "username": logged_in_user.username,
             "about": logged_in_user.about})

    def on_failure(self, message: str) -> None:
        self.response.status = falcon.HTTP_400
        self.response.body = message


class Controller(object):
    def __init__(self, user_repository: users.Repository) -> None:
        self.user_repository = user_repository

    def on_post(self, request: falcon.Request, response: falcon.Response) -> None:
        data = json.load(request.bounded_stream)
        presenter = Presenter(response)
        use_case = login.UseCase(self.user_repository, presenter)
        login_request = login.Request(data.get("username"), data.get("password"))
        use_case.execute(login_request)
