import falcon

import social_network.repositories.users
from social_network.apis import register_user_api


def create():
    api = falcon.API()
    user_repository = social_network.repositories.users.InMemoryRepository()
    api.add_route("/registration", register_user_api.Controller(user_repository))
    return api
