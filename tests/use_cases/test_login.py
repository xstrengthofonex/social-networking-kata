import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.repositories import users
from social_network.entities import user
from social_network.use_cases import login
from social_network.use_cases import base


class LoginTest(unittest.TestCase):
    USER_ID = user.Id(str(uuid4()))
    USERNAME = "Username"
    PASSWORD = "password"
    ABOUT = "About User"
    USER = user.User(USER_ID, USERNAME, PASSWORD, ABOUT)

    def setUp(self) -> None:
        self.repository = Mock(users.Repository)
        self.presenter = Mock(base.OutputBoundary)
        self.use_case = login.UseCase(self.repository, self.presenter)

    def test_login(self):
        self.given_matching_credentials_for(self.USER)
        request = login.Request(self.USERNAME, self.PASSWORD)

        self.use_case.execute(request)

        response = login.Response(self.USER_ID, self.USERNAME,  self.ABOUT)
        self.presenter.on_success.assert_called_with(response)
        self.repository.find_by_credentials.assert_called_with(self.USERNAME, self.PASSWORD)

    def test_failed_login(self):
        self.given_no_matching_credentials()
        request = login.Request(self.USERNAME, "wrong.PASSWORD")

        self.use_case.execute(request)
      
        self.presenter.on_failure.assert_called_with(login.INVALID_CREDENTIALS)
        self.repository.find_by_credentials.assert_called_with(self.USERNAME, "wrong.PASSWORD")

    def given_matching_credentials_for(self, a_user: user.User):
        self.repository.find_by_credentials.return_value = a_user

    def given_no_matching_credentials(self):
        self.repository.find_by_credentials.return_value = None
