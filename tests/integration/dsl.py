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
