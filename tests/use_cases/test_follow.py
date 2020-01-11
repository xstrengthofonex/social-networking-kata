import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.repositories import users
from social_network.entities import user
from social_network.use_cases import follow


class FollowTest(unittest.TestCase):
    FOLLOWER_USER = user.User(
        id=user.Id(str(uuid4())),
        username="Follower",
        password="password",
        about="I follow people")
    FOLLOWEE_USER = user.User(
        id=user.Id(str(uuid4())),
        username="Followee",
        password="password",
        about="I'm followed by people")
   
    def setUp(self) -> None:
        self.repository = users.InMemoryRepository()
        self.presenter = Mock(follow.Presenter)
        self.use_case = follow.UseCase(self.repository, self.presenter)

    def test_follow(self):
        self.repository.add(self.FOLLOWER_USER)
        self.repository.add(self.FOLLOWEE_USER)

        self.use_case.execute(follow.Request(self.FOLLOWER_USER.id, self.FOLLOWEE_USER.id))

        self.assertEqual([self.FOLLOWER_USER], self.repository.get_followers_for(self.FOLLOWEE_USER.id))
        self.presenter.on_success.assert_called()

    def test_cannot_create_following_if_either_users_do_not_exist(self):
        self.use_case.execute(follow.Request(self.FOLLOWER_USER.id, "NonExistentId"))

        self.assertEqual([], self.repository.get_followers_for(self.FOLLOWER_USER.id))
        self.presenter.on_failure.assert_called_with(follow.USER_DOES_NOT_EXIST)
