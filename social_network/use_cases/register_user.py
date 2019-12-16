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


class UseCase(object):
    def __init__(self, presenter: Presenter, repository: user.Repository) -> None:
        self.repository = repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        pass
