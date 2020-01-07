from dataclasses import dataclass
from datetime import datetime
from typing import List

from social_network.entities import post
from social_network.entities import user
from social_network.repositories import posts
from social_network.repositories import users
from social_network.use_cases import base


@dataclass(frozen=True)
class Request(base.Request):
    user_id: str


@dataclass(frozen=True)
class PostDto(object):
    id: post.Id
    user_id: user.Id
    text: str
    created_on: datetime


@dataclass(frozen=True)
class Response(base.Response):
    posts: List[PostDto]


class UseCase(base.InputBoundary):
    def __init__(self, posts_repository: posts.Repository,
                 users_repository: users.Repository,
                 presenter: base.OutputBoundary):
        self.posts_repository = posts_repository
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        timeline = self.posts_repository.get_timeline_for_user(user.Id(request.user_id))
        response = self.create_response_from(timeline)
        self.presenter.on_success(response)

    @staticmethod
    def create_response_from(timeline: List[post.Post]) -> Response:
        return Response(posts=[
            PostDto(id=p.id, user_id=p.user_id, text=p.text,
                    created_on=p.created_on) for p in timeline])
