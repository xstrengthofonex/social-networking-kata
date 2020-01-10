import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.repositories import users
from social_network.entities import user
from social_network.use_cases import follow
from social_network.use_cases import base


class FollowTest(unittest.TestCase):
    FOLLOWER_USER_ID = user.Id(str(uuid4()))
    FOLLOWER_USERNAME = "Follower"
    FOLLOWER_PASSWORD = "password"
    FOLLOWER_ABOUT = "I'm following the leader"
    FOLLOWER_USER = user.User(FOLLOWER_USER_ID, FOLLOWER_USERNAME, FOLLOWER_PASSWORD, FOLLOWER_ABOUT)
    FOLLOWEE_USER_ID = user.Id(str(uuid4()))
    FOLLOWEE_USERNAME = "Followee"
    FOLLOWEE_PASSWORD = "password"
    FOLLOWEE_ABOUT = "About User"
    FOLLOWEE_USER = user.User(FOLLOWEE_USER_ID, FOLLOWEE_USERNAME, FOLLOWEE_PASSWORD, FOLLOWEE_ABOUT)
   
    def setUp(self) -> None:
        self.repository = users.InMemoryRepository
        self.presenter = Mock(base.OutputBoundary)
        self.use_case = follow.UseCase(self.repository, self.presenter)

    def test_follow(self):
        self.use_case.execute(follow.Request(self.FOLLOWER_USER, self.FOLLOWEE_USER))
        actualFollowers = self.repository.get_followers(self.FOLLOWEE_USER)              
        self.assertEquals(actualFollowers, [self.FOLLOWER_USER])