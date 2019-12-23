import falcon

from social_network.domain import user
from social_network.use_cases import register_user
from social_network.use_cases.register_user import Response


class Presenter(register_user.Presenter):
    def on_success(self, response: Response) -> None:
        pass

    def on_failure(self, message: str) -> None:
        pass


class Controller(object):
    def __init__(self, user_repository: user.Repository):
        self.user_repository = user_repository

    def on_post(self, request: falcon.Request, response: falcon.Response) -> None:
        raise NotImplementedError
