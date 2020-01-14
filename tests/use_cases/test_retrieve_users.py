import unittest
from unittest.mock import Mock
from uuid import uuid4

from social_network.common import boundary
from social_network.common import dto
from social_network.users import user
from social_network.users import users
from social_network.users.use_cases import retrieve_users


class RetrieveWallTest(unittest.TestCase):
    USER_A = user.User(id=user.Id(str(uuid4())), username="User A", password="password", about="About User A")
    USER_B = user.User(id=user.Id(str(uuid4())), username="User B", password="password", about="About User B")
    USER_C = user.User(id=user.Id(str(uuid4())), username="User C", password="password", about="About User C")

    def setUp(self) -> None:
        self.presenter = Mock(boundary.Output)
        self.users_repository = users.InMemoryRepository()
        self.use_case = retrieve_users.UseCase(self.users_repository, self.presenter)

    def test_retrieve_users_when_there_are_no_users(self):
        self.use_case.execute()
        response = retrieve_users.Response([])
        self.presenter.on_success.assert_called_with(response)

    def test_retrieve_users_when_there_are_three_users(self):
        self.users_repository.add(self.USER_A)
        self.users_repository.add(self.USER_B)
        self.users_repository.add(self.USER_C)
        self.use_case.execute()

        response = retrieve_users.Response([
            self.user_to_dto(u) for u in [self.USER_A, self.USER_B, self.USER_C]])
        self.presenter.on_success.assert_called_with(response)

    @staticmethod
    def user_to_dto(a_user: user.User) -> dto.User:
        return dto.User(id=a_user.id, username=a_user.username, about=a_user.about)
