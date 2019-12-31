import json

import falcon

from social_network.repositories import users
from social_network.use_cases import login


class Presenter(login.Presenter):
    def on_success(self, logged_in_user: login.Response) -> None:
        pass

    def on_failure(self, error: str) -> None:
        pass


class Controller(object):
    def __init__(self, user_repository: users.Repository):
        self.user_repository = user_repository

    def on_post(self, request: falcon.Request, response: falcon.Response) -> None:
        response.body = json.dumps(dict())
