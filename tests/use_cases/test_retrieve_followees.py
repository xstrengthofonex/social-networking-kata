from unittest.mock import Mock
from uuid import uuid4

from social_network.users import users, user
from social_network.users.use_cases import retrieve_followees
from tests.use_cases import base


class RetrieveFolloweesTest(base.UseCaseTest):
    USER = user.User(id=user.Id(str(uuid4())), username="User", password="password", about="About User")
    FOLLOWEE_1 = user.User(
        id=user.Id(str(uuid4())), username="Followee1", password="password", about="About Followee1")
    FOLLOWEE_2 = user.User(
        id=user.Id(str(uuid4())), username="Followee2", password="password", about="About Followee2")

    def setUp(self) -> None:
        self.users_repository = users.InMemoryRepository()
        self.presenter = Mock(retrieve_followees.Presenter)
        self.use_case = retrieve_followees.UseCase(self.users_repository, self.presenter)

    def test_retrieve_all_followees_for_user(self):
        self.users_repository.add(self.USER)
        self.users_repository.add(self.FOLLOWEE_1)
        self.users_repository.add(self.FOLLOWEE_2)
        self.users_repository.add_follower(user.FollowerId(self.USER.id), user.FolloweeId(self.FOLLOWEE_1.id))
        self.users_repository.add_follower(user.FollowerId(self.USER.id), user.FolloweeId(self.FOLLOWEE_2.id))

        self.use_case.execute(retrieve_followees.Request(user_id=str(self.USER.id)))

        self.presenter.on_success.assert_called_with(retrieve_followees.Response(
            [self.user_to_dto(u) for u in [self.FOLLOWEE_1, self.FOLLOWEE_2]]))
