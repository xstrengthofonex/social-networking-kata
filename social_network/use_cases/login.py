from abc import ABC, abstractmethod
from dataclasses import dataclass

import social_network.repositories.users
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


class UseCase(object):
    def __init__(self, presenter: Presenter, user_repository: social_network.repositories.users.Repository) -> None:
        self.user_repository = user_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        found_user = self.user_repository.find_by_credentials(request.username, request.password)
        if not found_user:
            self.presenter.on_failure(INVALID_CREDENTIALS)
        else:
            response = Response(found_user.id, found_user.username, found_user.about)
            self.presenter.on_success(response)
