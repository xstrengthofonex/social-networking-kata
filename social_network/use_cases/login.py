from abc import ABC, abstractmethod
from .base import BaseUseCase
from dataclasses import dataclass
from social_network.repositories import users
from social_network.entities import user


INVALID_CREDENTIALS = "Invalid Credentials"


@dataclass(frozen=True)
class Request(object):
    username: str
    password: str


@dataclass(frozen=True)
class Response:
    user_id: user.Id
    username: str
    about: str


class Presenter(ABC):
    @abstractmethod
    def on_success(self, response: Response) -> None:
        pass

    @abstractmethod
    def on_failure(self, error: str) -> None:
        pass


class UseCase(BaseUseCase):
    def __init__(self, presenter: Presenter, users_repository: users.Repository) -> None:
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        found_user = self.users_repository.find_by_credentials(request.username, request.password)
        if not found_user:
            self.presenter.on_failure(INVALID_CREDENTIALS)
        else:
            response = Response(found_user.id, found_user.username, found_user.about)
            self.presenter.on_success(response)
