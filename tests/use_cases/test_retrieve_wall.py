import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

from social_network.entities import post
from social_network.entities import user
from social_network.repositories import users
from social_network.repositories import posts
from social_network.use_cases import base
from social_network.use_cases import retrieve_wall


class RetrieveWallTest(unittest.TestCase):
    USER_ID = user.Id(str(uuid4()))
    FOLLOWER_ID = user.Id(str(uuid4()))
    POST_1 = post.Post(post.Id(str(uuid4())), USER_ID, "post 1", Mock(datetime))
    F_POST_1 = post.Post(post.Id(str(uuid4())), FOLLOWER_ID, "follower post 1", Mock(datetime))
    
    def setUp(self) -> None:
        self.presenter =  Mock(base.OutputBoundary)
        self.repository = posts.InMemoryRepository()
        self.w_user_id = self.USER_ID
        
    
    def test_user_with_no_posts_and_no_followers_has_no_posts_on_wall(self):
        use_case = retrieve_wall.UseCase(self.repository, self.presenter)
        use_case.execute(retrieve_wall.Request(self.w_user_id))
        response = retrieve_wall.Response([])
        self.presenter.on_success.assert_called_with(response)
        
    def test_user_with_one_post_and_no_followers_has_one_post_on_wall(self):
        self.repository.add(self.POST_1)
        use_case = retrieve_wall.UseCase(self.repository, self.presenter)
        use_case.execute(retrieve_wall.Request(self.w_user_id))
        response = retrieve_wall.Response([self.POST_1])
        self.presenter.on_success.assert_called_with(response)
        
    def test_user_with_one_post_and_one_followers_has_two_post_on_wall(self):
        self.repository.add(self.POST_1)
        use_case = retrieve_wall.UseCase(self.repository, self.presenter)
        use_case.execute(retrieve_wall.Request(self.w_user_id))
        response = retrieve_wall.Response([self.POST_1, self.F_POST_1])
        self.presenter.on_success.assert_called_with(response)