import falcon

from social_network.apis.create_post_api import CreatePostAPI
from social_network.apis.follow_user_api import FollowUserAPI
from social_network.apis.login_api import LoginAPI
from social_network.apis.register_user_api import RegisterUserAPI
from social_network.apis.retrieve_timeline_api import RetrieveTimelineAPI
from social_network.apis.retrieve_wall_api import RetrieveWallAPI
from social_network.repositories import users
from social_network.repositories import posts


def create():
    api = falcon.API()
    user_repository = users.InMemoryRepository()
    post_repository = posts.InMemoryRepository()
    api.add_route("/registration", RegisterUserAPI(user_repository))
    api.add_route("/login", LoginAPI(user_repository))
    api.add_route("/users/{user_id}/posts", CreatePostAPI(post_repository, user_repository))
    api.add_route("/users/{user_id}/timeline", RetrieveTimelineAPI(post_repository, user_repository))
    api.add_route("/users/{user_id}/wall", RetrieveWallAPI(post_repository, user_repository))
    api.add_route("/follow", FollowUserAPI(user_repository))
    return api

