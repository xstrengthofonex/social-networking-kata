from abc import ABC, abstractmethod
from dataclasses import dataclass


from social_network.entities import user
from social_network.repositories import users

REGISTRATION_ERROR = "Username already in use"


@dataclass(frozen=True)
class Request(object):
    username: str
    password: str
    about: str


@dataclass(frozen=True)
class Response(object):
    user_id: str
    username: str
    about: str


class Presenter(ABC):
    @abstractmethod
    def on_success(self, response: Response) -> None:
        pass

    @abstractmethod
    def on_failure(self, message: str) -> None:
        pass


class InputBoundary(ABC):
    @abstractmethod
    def execute(self, request: Request) -> None:
        pass


class UseCase(object):
    def __init__(self, users_repository: users.Repository, presenter: Presenter) -> None:
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


