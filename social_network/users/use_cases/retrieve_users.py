from dataclasses import dataclass

from social_network.infrastructure import base
from social_network.users import users


@dataclass(frozen=True)
class Response(base.Response):
    users: list


class UseCase(base.InputBoundary):

    def __init__(self, users_repository: users.Repository, presenter: base.OutputBoundary) -> None:
        self.users = users_repository
        self.presenter = presenter

    def execute(self, request: base.Request) -> None:
        all_users = self.users.get_all_users()
        self.presenter.on_success(Response(all_users))
