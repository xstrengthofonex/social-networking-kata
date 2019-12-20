from abc import ABC, abstractmethod
from dataclasses import dataclass

from social_network.domain import user


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


class UseCase(object):
    def __init__(self, presenter: Presenter, user_repository: user.Repository) -> None:
        self.user_repository = user_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        if self.user_repository.username_exists(request.username):
            self.presenter.on_failure("Username already in use.")
        else:
            new_user = self.create_new_user_from(request)
            self.user_repository.add(new_user)
            response = Response(new_user.id, new_user.username, new_user.about)
            self.presenter.on_success(response)

    def create_new_user_from(self, request: Request) -> user.User:
        return user.User(
            user.Id(self.user_repository.get_next_id()),
            request.username,
            request.password,
            request.about)
