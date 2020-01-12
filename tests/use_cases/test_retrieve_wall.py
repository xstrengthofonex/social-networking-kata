import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

from social_network.entities import post
from social_network.entities import user
from social_network.repositories import users
from social_network.repositories import posts
from social_network.use_cases import base
from social_network.use_cases import dto
from social_network.use_cases import retrieve_wall


class RetrieveWallTest(unittest.TestCase):
    USER_ID = user.Id(str(uuid4()))
    FOLLOWEE_ID = user.Id(str(uuid4()))
    TODAY = datetime.now()
    YESTERDAY = datetime.now() - timedelta(days=1)
    USER = user.User(id=USER_ID, username="User", password="password", about="About User")
    FOLLOWEE = user.User(id=FOLLOWEE_ID, username="Followee", password="password", about="About Followee")
    POST_1 = dto.Post(id=USER_ID, user_id=USER_ID, text="post 1", created_on=YESTERDAY)
    POST_2 = dto.Post(id=FOLLOWEE_ID, user_id=FOLLOWEE_ID, text="follower post 1", created_on=TODAY)
    
    def setUp(self) -> None:
        self.presenter = Mock(base.OutputBoundary)
        self.posts_repository = posts.InMemoryRepository()
        self.users_repository = users.InMemoryRepository()
        self.use_case = retrieve_wall.UseCase(self.posts_repository, self.users_repository, self.presenter)
        self.users_repository.add(self.USER)
        self.users_repository.add(self.FOLLOWEE)
        self.users_repository.add_follower(self.USER_ID, self.FOLLOWEE_ID)

    def test_user_with_no_posts_and_no_followers_has_no_posts_on_wall(self):
        self.use_case.execute(retrieve_wall.Request(self.USER_ID))

        response = retrieve_wall.Response([])
        self.presenter.on_success.assert_called_with(response)
        
    def test_user_with_one_post_and_no_followers_has_one_post_on_wall(self):
        self.posts_repository.add(self.POST_1)

        self.use_case.execute(retrieve_wall.Request(self.USER_ID))

        response = retrieve_wall.Response([self.POST_1])
        self.presenter.on_success.assert_called_with(response)
        
    def test_user_with_one_post_and_one_followers_has_two_post_on_wall(self):
        self.posts_repository.add(self.POST_2)
        self.posts_repository.add(self.POST_1)

        self.use_case.execute(retrieve_wall.Request(self.USER_ID))

        response = retrieve_wall.Response([self.POST_2, self.POST_1])
        self.presenter.on_success.assert_called_with(response)
