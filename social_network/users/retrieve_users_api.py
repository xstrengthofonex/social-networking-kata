import json

import falcon

from social_network.infrastructure import base
from social_network.users import users
from social_network.users.use_cases import retrieve_users


class Presenter(base.OutputBoundary):
    def __init__(self, response: falcon.Response) -> None:
        self.response = response

    def on_success(self, all_users_response: retrieve_users.Response) -> None:
        self.response.content_type = "application/json"
        self.response.status = falcon.HTTP_200
        self.response.body = json.dumps([
            dict(id=u.id,
                 username=u.username,
                 about=u.about
                 )
            for u in all_users_response.users])

    def on_failure(self, response: retrieve_users.Response) -> None:
        # never called
        pass


class RetrieveUsersAPI(object):
    def __init__(self, user_repository: users.Repository):
        self.user_repository = user_repository

    def on_get(self, request: falcon.Request, response: falcon.Response) -> None:
        presenter = Presenter(response)
        retrieve_users.UseCase(self.user_repository, presenter).execute(base.Request())
