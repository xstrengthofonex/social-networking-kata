import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.domain import user
from social_network.use_cases import register_user


class RegisterUserTest(unittest.TestCase):
    USER_ID = user.Id(str(uuid4()))
    USERNAME = "Username"
    PASSWORD = "password"
    ABOUT = "About User"
    USER = user.User(USER_ID, USERNAME, PASSWORD, ABOUT)

    def setUp(self) -> None:
        self.presenter = Mock(register_user.Presenter)
        self.repository = Mock(user.Repository)
        self.use_case = register_user.UseCase(self.presenter, self.repository)

    def test_register_user(self):
        self.repository.get_next_id.return_value = self.USER_ID
        request = register_user.Request(self.USERNAME, self.PASSWORD, self.ABOUT)
        response = register_user.Response(self.USER_ID, self.USERNAME, self.ABOUT)

        self.use_case.execute(request)

        self.presenter.on_success.assert_called_with(response)
        self.repository.add.assert_called_with(self.USER)
