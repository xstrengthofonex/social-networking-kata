import falcon

from social_network.repositories import users, posts
from social_network.apis import (
    register_user_api,
    login_api,
    create_post_api,
    retrieve_timeline_api,
    follow_user_api)


def create():
    api = falcon.API()
    user_repository = users.InMemoryRepository()
    post_repository = posts.InMemoryRepository()
    api.add_route("/registration", register_user_api.Controller(user_repository))
    api.add_route("/login", login_api.Controller(user_repository))
    api.add_route("/users/{user_id}/posts", create_post_api.Controller(post_repository, user_repository))
    api.add_route("/users/{user_id}/timeline", retrieve_timeline_api.Controller(post_repository, user_repository))
    api.add_route("/follow", follow_user_api.Controller(user_repository))
    return api
