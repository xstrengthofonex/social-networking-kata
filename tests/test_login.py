import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.domain import user
from social_network.use_cases import login


class LoginTest(unittest.TestCase):
    USER_ID = user.Id(str(uuid4()))
    USERNAME = "Username"
    PASSWORD = "password"
    ABOUT = "About User"
    USER = user.User(USER_ID, USERNAME, PASSWORD, ABOUT)

    def setUp(self) -> None:
        self.repository = Mock(user.Repository)
        self.presenter = Mock(login.Presenter)
        self.use_case = login.UseCase(self.presenter,self.repository)

    def test_login(self):
        self.repository.find_by_credentials.return_value = self.USER
        request = login.Request(self.USERNAME, self.PASSWORD)

        self.use_case.execute(request)

        response = login.Response(self.USER_ID, self.USERNAME,  self.ABOUT)
        self.presenter.on_success.assert_called_with(response)
        self.repository.find_by_credentials.assert_called_with(self.USERNAME, self.PASSWORD)
    def test_failed_login(self):
        self.repository.find_by_credentials.return_value = self.USER
        request = login.Request(self.USERNAME, "wrong.PASSWORD")

        self.use_case.execute(request)
      
        self.presenter.on_failure.assert_called_with( login.INVALID_CREDENTIALS)
        self.repository.find_by_credentials.assert_called_with(self.USERNAME, "wrong.PASSWORD")
