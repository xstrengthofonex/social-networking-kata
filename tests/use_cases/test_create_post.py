import unittest
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

from social_network.infrastructure import base
from social_network.posts import post, posts
from social_network.posts.use_cases import create_post
from social_network.users import user, users


class CreatePostTest(unittest.TestCase):
    TEXT = "Some text"
    USER_ID = user.Id(str(uuid4()))
    POST_ID = post.Id(str(uuid4()))
    DATETIME = datetime.now()
    POST = post.Post(id=POST_ID, user_id=USER_ID, text=TEXT, created_on=DATETIME)
    USER = user.User(id=USER_ID, username="Username", password="password", about="About user")

    def setUp(self) -> None:
        self.posts_repository = Mock(posts.Repository)
        self.users_repository = Mock(users.Repository)
        self.clock = Mock(datetime)
        self.presenter = Mock(base.OutputBoundary)
        self.use_case = create_post.UseCase(
            self.posts_repository, self.users_repository,
            self.presenter, self.clock)

    def test_create_post(self):
        request = create_post.Request(user_id=self.USER_ID, text=self.TEXT)
        self.posts_repository.get_next_id.return_value = self.POST_ID
        self.users_repository.find_by_id.return_value = self.USER
        self.clock.now.return_value = self.DATETIME

        self.use_case.execute(request)

        response = create_post.Response(
            post_id=self.POST_ID, user_id=self.USER_ID,
            text=self.TEXT, created_on=self.DATETIME)
        self.presenter.on_success.assert_called_with(response)
        self.posts_repository.add.assert_called_with(self.POST)

    def test_do_not_create_post_if_invalid_user(self):
        request = create_post.Request(user_id=self.USER_ID, text=self.TEXT)
        self.posts_repository.get_next_id.return_value = self.POST_ID
        self.users_repository.find_by_id.return_value = None

        self.use_case.execute(request)

        response = create_post.USER_DOES_NOT_EXIST
        self.presenter.on_failure.assert_called_with(response)
        self.posts_repository.add.assert_not_called()

