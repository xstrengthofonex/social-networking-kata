import json

import falcon

from social_network.repositories import users
from social_network.repositories import posts
from social_network.use_cases import retrieve_wall

class RetrieveWallAPI(object):
    def __init__(self, posts_repository: posts.Repository, users_repository: users.Repository):
        self.posts_repository = posts_repository
        self.users_repository = users_repository

    def on_get(self, request: falcon.Request, response: falcon.Response, user_id: str) -> None:
        use_case = retrieve_wall.UseCase()
        use_case.execute(retrieve_wall.Request(request))
        response.body = json.dumps([])
