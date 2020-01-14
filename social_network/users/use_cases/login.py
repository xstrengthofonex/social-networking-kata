from dataclasses import dataclass

from social_network.common import boundary
from social_network.users import user
from social_network.users import users


INVALID_CREDENTIALS = "Invalid Credentials"


@dataclass(frozen=True)
class Request(boundary.Request):
    username: str
    password: str


@dataclass(frozen=True)
class Response(boundary.Response):
    user_id: user.Id
    username: str
    about: str


class UseCase(boundary.Input):
    def __init__(self, users_repository: users.Repository, presenter: boundary.Output) -> None:
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        found_user = self.users_repository.find_by_credentials(request.username, request.password)
        if not found_user:
            self.presenter.on_failure(INVALID_CREDENTIALS)
        else:
            response = Response(found_user.id, found_user.username, found_user.about)
            self.presenter.on_success(response)
