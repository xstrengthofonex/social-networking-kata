import falcon

from social_network.repositories import users
from social_network.apis import register_user_api


def create():
    api = falcon.API()
    user_repository = users.InMemoryRepository()
    api.add_route("/registration", register_user_api.Controller(user_repository))
    return api
