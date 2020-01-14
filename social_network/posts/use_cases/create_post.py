from dataclasses import dataclass
from datetime import datetime

from social_network.common import boundary
from social_network.posts import post
from social_network.posts import posts
from social_network.users import user
from social_network.users import users


@dataclass(frozen=True)
class Request(boundary.Request):
    user_id: str
    text: str


@dataclass(frozen=True)
class Response(boundary.Response):
    post_id: post.Id
    user_id: user.Id
    text: str
    created_on: datetime


USER_DOES_NOT_EXIST = "User Does Not Exist."


class UseCase(boundary.Input):
    def __init__(self, posts_repository: posts.Repository,
                 users_repository: users.Repository,
                 presenter: boundary.Output,
                 clock: datetime):
        self.posts_repository = posts_repository
        self.users_repository = users_repository
        self.presenter = presenter
        self.clock = clock

    def execute(self, request: Request) -> None:
        if not self.users_repository.find_by_id(user.Id(request.user_id)):
            self.presenter.on_failure(USER_DOES_NOT_EXIST)
        else:
            new_post: post.Post = self.create_new_post_from(request)
            self.posts_repository.add(new_post)
            response = Response(new_post.id, new_post.user_id, new_post.text, new_post.created_on)
            self.presenter.on_success(response)

    def create_new_post_from(self, request: Request) -> post.Post:
        return post.Post(
            id=self.posts_repository.get_next_id(),
            user_id=user.Id(request.user_id),
            text=request.text,
            created_on=self.clock.now())
