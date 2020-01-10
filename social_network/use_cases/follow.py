from dataclasses import dataclass
from datetime import datetime

from social_network.entities import post
from social_network.entities import user
from social_network.infrastructure.clock import Clock
from social_network.repositories import posts
from social_network.repositories import users
from social_network.use_cases import base


@dataclass(frozen=True)
class Request(base.Request):
    follower_id: str
    followee_id: str


@dataclass(frozen=True)
class Response(base.Response):
    text: str



USER_DOES_NOT_EXIST = "At least one of the users does not exist."


class UseCase(base.InputBoundary):
    def __init__(self,
                 users_repository: users.Repository,
                 presenter: base.OutputBoundary
                 ):
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        if not self.users_repository.find_by_id(user.Id(request.follower_id)) or not self.users_repository.find_by_id(user.Id(request.followee_id)):
            self.presenter.on_failure(USER_DOES_NOT_EXIST)
        else:
            self.users_repository.add_follower(request.follower_id, request.followee_id)
            self.presenter.on_success()

    