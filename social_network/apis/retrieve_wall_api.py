import json

import falcon

from social_network.repositories import users
from social_network.repositories import posts


class RetrieveWallAPI(object):
    def __init__(self, posts_repository: posts.Repository, users_repository: users.Repository):
        self.posts_repository = posts_repository
        self.users_repository = users_repository

    def on_get(self, request: falcon.Request, response: falcon.Response, user_id: str) -> None:
        response.body = json.dumps([])
