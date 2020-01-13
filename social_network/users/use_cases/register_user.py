from dataclasses import dataclass

from social_network.infrastructure import base
from social_network.users import user, users

REGISTRATION_ERROR = "Username already in use"


@dataclass(frozen=True)
class Request(base.Request):
    username: str
    password: str
    about: str


@dataclass(frozen=True)
class Response(base.Response):
    user_id: str
    username: str
    about: str


class UseCase(base.InputBoundary):
    def __init__(self, users_repository: users.Repository, presenter: base.OutputBoundary) -> None:
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        if self.users_repository.username_exists(request.username):
            self.presenter.on_failure(REGISTRATION_ERROR)
        else:
            new_user = self.create_new_user_from(request)
            self.users_repository.add(new_user)
            response = Response(new_user.id, new_user.username, new_user.about)
            self.presenter.on_success(response)

    def create_new_user_from(self, request: Request) -> user.User:
        return user.User(
            user.Id(self.users_repository.get_next_id()),
            request.username,
            request.password,
            request.about)


