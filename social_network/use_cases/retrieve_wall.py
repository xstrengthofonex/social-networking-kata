from dataclasses import dataclass
from typing import List

from social_network.entities import user
from social_network.use_cases import base
from social_network.use_cases import dto
from social_network.repositories import posts
from social_network.repositories import users


@dataclass(frozen=True)
class Request(base.Request):
    user_id: str


@dataclass(frozen=True)
class Response(base.Response):
    posts: List[dto.Post]


class UseCase(base.InputBoundary):
    def __init__(self, posts_repository: posts.Repository,
                 users_repository: users.Repository,
                 presenter: base.OutputBoundary):
        self.presenter = presenter
        self.users_repository = users_repository
        self.posts_repository = posts_repository

    def execute(self, request: Request) -> None:
        if not self.users_repository.find_by_id(user.Id(request.user_id)):
            self.presenter.on_failure("User does not exist.")
        else:
            followees = self.users_repository.find_followees_for(user.FollowerId(user.Id(request.user_id)))
            user_posts = self.posts_repository.get_timeline_for_user(user.Id(request.user_id))
            followee_posts = [self.posts_repository.get_timeline_for_user(f.id) for f in followees]
            for p in followee_posts:
                user_posts.extend(p)
            response = self.create_response_from_posts(user_posts)
            self.presenter.on_success(response)

    @staticmethod
    def create_response_from_posts(user_posts):
        response = Response([
            dto.Post(id=p.id, user_id=p.user_id, text=p.text, created_on=p.created_on)
            for p in sorted(user_posts, key=lambda u: u.created_on, reverse=True)])
        return response
