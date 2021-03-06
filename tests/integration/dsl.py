import logging
import time
import unittest
from dataclasses import dataclass
from typing import Dict, List

import webtest

from social_network import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dsl.APITest")


@dataclass
class User(object):
    id: str = None
    username: str = "Username"
    password: str = "password"
    about: str = "About"


@dataclass
class Post(object):
    post_id: str
    user_id: str
    text: str
    date: str
    time: str


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

    def create_registered_user(self, username: str = "User") -> User:
        user = User(username=username)
        self.register_user(user)
        logger.info(f"Created user: {user}")
        return user

    def create_post(self, user_id: str, text: str) -> Post:
        logger.info(f"Creating post for {user_id} with text: '{text}'")
        create_post_data = dict(user_id=user_id, text=text)
        response = self.client.post_json(f"/users/{user_id}/posts", params=create_post_data)
        post = Post(post_id=response.json.get("postId"),
                    user_id=response.json.get("userId"),
                    text=response.json.get("text"),
                    date=response.json.get("date"),
                    time=response.json.get("time"))
        logger.info(f"Post created: {post}")
        time.sleep(0.1)  # A brief sleep is required to enabled sort by time
        return post

    def create_following(self, follower_id: str, followee_id: str):
        logger.info(f"Creating following for {follower_id} and {followee_id}")
        follow_request_data = dict(followerId=follower_id, followeeId=followee_id)
        response = self.client.post_json("/follow", params=follow_request_data)
        logger.info(f"Following created for {follower_id} and {followee_id}")
        return response

    @staticmethod
    def json_user_to_dsl_user(json_user: Dict[str, str]) -> User:
        return User(
            id=json_user.get("id"),
            username=json_user.get("username"),
            about=json_user.get("about"))

    def json_users_to_dsl_users(self, json_users: List[Dict[str, str]]) -> List[User]:
        return [self.json_user_to_dsl_user(u) for u in json_users]