import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.common import boundary
from social_network.users import user
from social_network.users import users
from social_network.users.use_cases import register_user


class RegisterUserTest(unittest.TestCase):
    USER_ID = user.Id(str(uuid4()))
    USERNAME = "Username"
    PASSWORD = "password"
    ABOUT = "About User"
    USER = user.User(USER_ID, USERNAME, PASSWORD, ABOUT)
    DUPLICATE_USERNAME = "DuplicateUserName"
    DUPLICATE_USER = user.User(USER_ID, DUPLICATE_USERNAME, PASSWORD, ABOUT)

    def setUp(self) -> None:
        self.presenter = Mock(boundary.Output)
        self.repository = Mock(users.Repository)
        self.use_case = register_user.UseCase(self.repository, self.presenter)

    def test_register_user(self):
        self.repository.username_exists.return_value = False
        self.repository.get_next_id.return_value = self.USER_ID
        request = register_user.Request(self.USERNAME, self.PASSWORD, self.ABOUT)

        self.use_case.execute(request)

        response = register_user.Response(self.USER_ID, self.USERNAME, self.ABOUT)
        self.presenter.on_success.assert_called_with(response)
        self.repository.add.assert_called_with(self.USER)

    def test_register_user_fails(self):
        self.repository.username_exists.return_value = True
        request = register_user.Request(self.DUPLICATE_USERNAME, self.PASSWORD, self.ABOUT)

        self.use_case.execute(request)

        self.repository.username_exists.assert_called_with(self.DUPLICATE_USERNAME)
        self.presenter.on_failure.assert_called_with(register_user.REGISTRATION_ERROR)
