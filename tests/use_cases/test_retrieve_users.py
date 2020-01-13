import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.infrastructure import base
from social_network.users import user, users
from social_network.users.use_cases import retrieve_users


class RetrieveWallTest(unittest.TestCase):
    USER_A = user.User(id=user.Id(str(uuid4())), username="User A", password="password", about="About User A")
    USER_B = user.User(id=user.Id(str(uuid4())), username="User B", password="password", about="About User B")
    USER_C = user.User(id=user.Id(str(uuid4())), username="User C", password="password", about="About User C")

    def setUp(self) -> None:
        self.presenter = Mock(base.OutputBoundary)
        self.users_repository = users.InMemoryRepository()
        self.use_case = retrieve_users.UseCase(self.users_repository, self.presenter)

    def test_retrieve_users_when_there_are_no_users(self):
        self.use_case.execute(base.Request())
        response = retrieve_users.Response([])
        self.presenter.on_success.assert_called_with(response)

    def test_retrieve_users_when_there_are_three_users(self):
        self.users_repository.add(self.USER_A)
        self.users_repository.add(self.USER_B)
        self.users_repository.add(self.USER_C)
        self.use_case.execute(base.Request())

        response = retrieve_users.Response([self.USER_A, self.USER_B, self.USER_C])
        self.presenter.on_success.assert_called_with(response)


