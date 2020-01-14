from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from social_network.common import boundary
from social_network.common import dto
from social_network.users import users
from social_network.users import user


@dataclass(frozen=True)
class Request(boundary.Request):
    user_id: str


@dataclass(frozen=True)
class Response(boundary.Response):
    followees: List[dto.User]


class Presenter(ABC):
    @abstractmethod
    def on_success(self, response: Response) -> None:
        pass


class UseCase(boundary.Input):
    def __init__(self, users_repository: users.Repository, presenter: Presenter):
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        followees = self.users_repository.find_followees_for(user.FollowerId(user.Id(request.user_id)))
        self.presenter.on_success(Response([dto.User(
            id=str(u.id), username=u.username, about=u.about)
            for u in followees]))
