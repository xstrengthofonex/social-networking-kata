from abc import ABC
from dataclasses import dataclass

from social_network.domain import user


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
    def on_success(self, response: Response) -> None:
        pass


class UseCase(object):
    def __init__(self, user_repository: user.Repository) -> None:
        self.user_repository = user_repository

    def execute(self, request: Request) -> None:
        pass
