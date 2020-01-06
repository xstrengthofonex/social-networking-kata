import falcon

from social_network.repositories import users, posts
from social_network.apis import register_user_api, login_api, post_api


def create():
    api = falcon.API()
    user_repository = users.InMemoryRepository()
    post_repository = posts.InMemoryRepository()
    api.add_route("/registration", register_user_api.Controller(user_repository))
    api.add_route("/login", login_api.Controller(user_repository))
    api.add_route("/users/{user_id}/posts", post_api.Controller(post_repository, user_repository))
    return api
