from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from social_network.common import boundary
from social_network.common import dto
from social_network.users import users


@dataclass(frozen=True)
class Response(boundary.Response):
    users: List[dto.User]


class Presenter(ABC):
    @abstractmethod
    def on_success(self, response: Response) -> None:
        pass


class InputBoundary(ABC):
    def execute(self) -> None:
        pass


class UseCase(InputBoundary):
    def __init__(self, users_repository: users.Repository, presenter: Presenter) -> None:
        self.users = users_repository
        self.presenter = presenter

    def execute(self) -> None:
        all_users = self.users.get_all_users()
        self.presenter.on_success(Response([
            dto.User(id=u.id, username=u.username, about=u.about) for u in all_users]))
