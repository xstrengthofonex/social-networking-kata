from abc import ABC, abstractmethod
from dataclasses import dataclass

from social_network.common import boundary
from social_network.users import user
from social_network.users import users


@dataclass(frozen=True)
class Request(boundary.Request):
    follower_id: str
    followee_id: str


@dataclass(frozen=True)
class Response(boundary.Response):
    text: str


class Presenter(ABC):
    @abstractmethod
    def on_success(self) -> None:
        pass

    @abstractmethod
    def on_failure(self, error: str) -> None:
        pass


USER_DOES_NOT_EXIST = "At least one of the users does not exist."


class UseCase(boundary.Input):
    def __init__(self, users_repository: users.Repository, presenter: Presenter):
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        if any(self.users_repository.find_by_id(user.Id(user_id)) is None
               for user_id in [request.followee_id, request.follower_id]):
            self.presenter.on_failure(USER_DOES_NOT_EXIST)
        else:
            self.users_repository.add_follower(user.Id(request.follower_id), user.Id(request.followee_id))
            self.presenter.on_success()


