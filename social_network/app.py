import falcon

from social_network.apis import register_user_api
from social_network.repositories import in_memory


def create():
    api = falcon.API()
    user_repository = in_memory.UserRepository()
    api.add_route("/registration", register_user_api.Controller(user_repository))
    return api
