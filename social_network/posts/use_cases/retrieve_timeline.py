from dataclasses import dataclass
from typing import List

from social_network.common import dto
from social_network.common import boundary
from social_network.posts import post
from social_network.posts import posts
from social_network.users import user
from social_network.users import users


@dataclass(frozen=True)
class Request(boundary.Request):
    user_id: str


@dataclass(frozen=True)
class Response(boundary.Response):
    posts: List[dto.Post]


class UseCase(boundary.Input):
    def __init__(self, posts_repository: posts.Repository,
                 users_repository: users.Repository,
                 presenter: boundary.Output):
        self.posts_repository = posts_repository
        self.users_repository = users_repository
        self.presenter = presenter

    def execute(self, request: Request) -> None:
        valid_user = self.users_repository.find_by_id(user.Id(request.user_id))
        if valid_user:
            timeline = self.posts_repository.get_timeline_for_user(valid_user.id)
            response = self.create_response_from(timeline)
            self.presenter.on_success(response)
        else:
            self.presenter.on_failure("User does not exist.")

    def create_response_from(self, timeline: List[post.Post]) -> Response:
        return Response(posts=[
            self.create_dto_from(p)
            for p in sorted(timeline, key=lambda p: p.created_on, reverse=True)])

    @staticmethod
    def create_dto_from(p: post.Post) -> dto.Post:
        return dto.Post(id=p.id, user_id=p.user_id, text=p.text,
                        created_on=p.created_on)
