import unittest
from dataclasses import dataclass

import webtest

from social_network import app


@dataclass
class User(object):
    id: str = None
    username: str = "Username"
    password: str = "password"
    about: str = "About"


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.create()
        self.client = webtest.TestApp(self.app)

    def register_user(self, a_user: User) -> None:
        registration_data = dict(
            username=a_user.username,
            password=a_user.password,
            about=a_user.about)
        response = self.client.post_json("/registration", params=registration_data)
        a_user.id = response.json.get("userId")

    def create_registered_user(self, user: User = None) -> User:
        if user is None:
            user = User()
        self.register_user(user)
        return user
