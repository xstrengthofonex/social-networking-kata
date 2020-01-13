from social_network.use_cases import base
from social_network.repositories import users
from dataclasses import dataclass


@dataclass(frozen=True)
class Response(base.Response):
    users: list


class UseCase(base.InputBoundary):

    def __init__(self, users_repository: users.Repository, presenter: base.OutputBoundary) -> None:
        self.users = users_repository
        self.presenter = presenter

    def execute(self) -> None:
        all_users = self.users.get_all_users()
        self.presenter.on_success(Response(all_users))
