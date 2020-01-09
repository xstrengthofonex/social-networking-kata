import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

from social_network.entities import post
from social_network.entities import user
from social_network.repositories import users
from social_network.repositories import posts
from social_network.use_cases import base
from social_network.use_cases import retrieve_timeline


class RetrieveTimelineTest(unittest.TestCase):
    TEXT = "Some text"
    USER_ID = user.Id(str(uuid4()))
    FIRST_POST_ID = post.Id(str(uuid4()))
    SECOND_POST_ID = post.Id(str(uuid4()))
    DATETIME = datetime.now()
    LATER_DATETIME = DATETIME + timedelta(3)
    FIRST_POST = retrieve_timeline.PostDto(
        id=FIRST_POST_ID, user_id=USER_ID, text=TEXT, created_on=DATETIME)
    SECOND_POST = retrieve_timeline.PostDto(
        id=SECOND_POST_ID, user_id=USER_ID, text=TEXT, created_on=LATER_DATETIME)
    USER = user.User(id=USER_ID, username="Username", password="password", about="About user")
    NON_EXISTENT_USER_ID = "NoneExistentUser"

    def setUp(self) -> None:
        self.posts_repository = Mock(posts.Repository)
        self.users_repository = Mock(users.Repository)
        self.presenter = Mock(base.OutputBoundary)
        self.use_case = retrieve_timeline.UseCase(
            self.posts_repository, self.users_repository, self.presenter)

    def test_get_timeline_for_user(self):
        request = retrieve_timeline.Request(user_id=self.USER_ID)
        self.posts_repository.get_timeline_for_user.return_value = [self.FIRST_POST, self.SECOND_POST]
        self.users_repository.find_by_id.return_value = self.USER

        self.use_case.execute(request)

        response = retrieve_timeline.Response(posts=[self.FIRST_POST, self.SECOND_POST])
        self.presenter.on_success.assert_called_with(response)
        self.posts_repository.get_timeline_for_user.assert_called_with(self.USER.id)

    def test_should_present_error_if_user_does_not_exist(self):
        request = retrieve_timeline.Request(user_id=self.NON_EXISTENT_USER_ID)
        self.users_repository.find_by_id.return_value = None

        self.use_case.execute(request)

        self.users_repository.find_by_id.assert_called_with(self.NON_EXISTENT_USER_ID)
        self.presenter.on_failure.assert_called_with("User does not exist.")
        self.posts_repository.get_timeline_for_user.assert_not_called()
        
