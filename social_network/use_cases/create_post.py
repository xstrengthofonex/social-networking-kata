from dataclasses import dataclass
from datetime import datetime

from social_network.entities import post
from social_network.entities import user
from social_network.repositories import posts
from social_network.repositories import users
from social_network.use_cases import base


@dataclass(frozen=True)
class Request(base.Request):
    user_id: str
    text: str


@dataclass(frozen=True)
class Response(base.Response):
    post_id: post.Id
    user_id: user.Id
    text: str
    created_on: datetime


class UseCase(base.InputBoundary):
    def __init__(self, posts_repository: posts.Repository,
                 users_repository: users.Repository,
                 presenter: base.OutputBoundary,
                 clock: datetime):
        self.posts_repository = posts_repository
        self.users_repository = users_repository
        self.presenter = presenter
        self.clock = clock

    def execute(self, request: Request) -> None:
        new_post = post.Post(self.posts_repository.get_next_id(), request.user_id, request.text, self.clock.now())
        self.posts_repository.add(new_post)
        response = Response(new_post.id, new_post.user_id, new_post.text, self.clock.now())
        self.presenter.on_success(response)
