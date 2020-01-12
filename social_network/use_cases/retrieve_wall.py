from dataclasses import dataclass

from social_network.use_cases import base
from social_network.entities import user
from social_network.repositories import posts

@dataclass(frozen=True)
class Request(base.Request):
    user_id : user.Id

@dataclass(frozen=True)
class Response(base.Response):
    posts : list


class UseCase(base.InputBoundary):
    def __init__(self, posts_repository: posts.Repository, presenter: base.OutputBoundary):
        self.presenter = presenter
        self.repository = posts_repository
        
        
    def execute(self, request: Request) -> None:
        posts = self.repository.get_timeline_for_user(request.user_id)
        response = Response(posts)
        self.presenter.on_success(response)
