from abc import ABC
from dataclasses import dataclass

from social_network.domain import user

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
    def on_success(self, response: Response) -> None:
        pass
    def on_failure(self, error: str) -> None:
        pass

class UseCase(object):
    def __init__(self,presenter:Presenter, user_repository: user.Repository) -> None:
        self.user_repository = user_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        user = self.user_repository.find_by_credentials(request.username, request.password)
        response = Response(user.id, user.username, user.about)
        self.presenter.on_success(response)
        
