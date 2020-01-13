from wsgiref.simple_server import make_server

import falcon

from social_network.posts import posts
from social_network.posts.create_post_api import CreatePostAPI
from social_network.posts.retrieve_timeline_api import RetrieveTimelineAPI
from social_network.posts.retrieve_wall_api import RetrieveWallAPI
from social_network.users import users
from social_network.users.follow_user_api import FollowUserAPI
from social_network.users.login_api import LoginAPI
from social_network.users.register_user_api import RegisterUserAPI
from social_network.users.retrieve_users_api import RetrieveUsersAPI


def create():
    api = falcon.API()
    user_repository = users.InMemoryRepository()
    post_repository = posts.InMemoryRepository()
    api.add_route("/registration", RegisterUserAPI(user_repository))
    api.add_route("/login", LoginAPI(user_repository))
    api.add_route("/users", RetrieveUsersAPI(user_repository))
    api.add_route("/users/{user_id}/posts", CreatePostAPI(post_repository, user_repository))
    api.add_route("/users/{user_id}/timeline", RetrieveTimelineAPI(post_repository, user_repository))
    api.add_route("/users/{user_id}/wall", RetrieveWallAPI(post_repository, user_repository))
    api.add_route("/follow", FollowUserAPI(user_repository))

    return api

def run(port=4321, host="localhost"):
    server = make_server(app=create(), host=host, port=port)
    print(f"serving at http://{host}:{port}")
    server.serve_forever()
