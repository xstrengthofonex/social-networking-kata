import json
import falcon

from social_network.domain import user
from social_network.use_cases import register_user


class Presenter(register_user.Presenter):
    def on_success(self, response: register_user.Response) -> None:
        pass

    def on_failure(self, message: str) -> None:
        pass


class Controller(object):
    def __init__(self, user_repository: user.Repository):
        self.user_repository = user_repository

    def on_post(self, request: falcon.Request, response: falcon.Response) -> None:
        data = json.load(request.bounded_stream)
        case = register_user.UseCase(self.user_repository, Presenter)
        ru_request = register_user.Request(data.get("username"), data.get("password"), data.get("about"))
        newUser = case.create_new_user_from(ru_request)
        response.content_type = "application/json"
        response.body = json.dumps({"id": newUser.id, "username": newUser.username, "about": newUser.about})
        response.status_int = 200

