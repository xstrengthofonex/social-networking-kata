import unittest

from social_network.common import dto
from social_network.users import user


class UseCaseTest(unittest.TestCase):
    @staticmethod
    def user_to_dto(a_user: user.User) -> dto.User:
        return dto.User(id=a_user.id, username=a_user.username, about=a_user.about)
