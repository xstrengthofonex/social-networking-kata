import json

import falcon

from social_network.users import users
from social_network.users.use_cases import retrieve_followees


class Presenter(retrieve_followees.Presenter):
    def __init__(self, response: falcon.Response):
        self.response = response

    def on_success(self, followees_response: retrieve_followees.Response) -> None:
        self.response.content_type = "application/json"
        self.response.body = json.dumps([
            dict(id=u.id, username=u.username, about=u.about)
            for u in followees_response.followees])


class RetrieveFolloweesAPI:
    def __init__(self, users_repository: users.Repository) -> None:
        self.users_repository = users_repository

    def on_get(self, request: falcon.Request, response: falcon.Response, user_id: str) -> None:
        use_case = retrieve_followees.UseCase(self.users_repository, Presenter(response))
        use_case.execute(retrieve_followees.Request(user_id))
