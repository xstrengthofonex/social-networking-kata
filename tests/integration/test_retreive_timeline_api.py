import webtest

from tests.integration import dsl
from social_network.entities import post
from social_network.entities import user
from social_network.use_cases.retrieve_timeline import PostDto
from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass

@dataclass(frozen=True)
class PresenterPost:
    post_id: post.Id
    user_id: user.Id
    text: str
    date: str
    time: str

class RetrieveTimelineAPITest(dsl.APITest):
    USER = dsl.User()
    TEXT = "Some text"
    POST = PresenterPost(str(uuid4()), USER.id, TEXT, datetime.now().date, datetime.now().time)

    def test_return_a_single_post_timeline_for_registered_user(self):
        registered_user = self.create_registered_user()
        self.create_post(registered_user.id, self.TEXT)
        response = self.retrieve_timeline_for_user(registered_user.id)
        self.assert_timeline(response, registered_user.id, self.POST)

    def create_post(self, user_id: str, text: str) -> webtest.TestResponse:
        create_post_data = dict(user_id=user_id, text=text)
        return self.client.post_json("/users/{user_id}/posts", params=create_post_data, status="*")
    
    def retrieve_timeline_for_user(self, user_id: str) -> webtest.TestResponse:
        return self.client.post_json("/users/{user_id}/timeline", status="*")

    def assert_timeline(self, response, user_id, post):
        self.assertEqual("200 OK", response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertEqual(post.post_id,response.json[0].get("post_id"))
        self.assertEqual(user_id, response.json[0].get("user_id"))
        self.assertEqual(post.text, response.json[0].get("text"))
        self.assertIsNotNone(response.json[0].get("date"))
        self.assertIsNotNone(response.json[0].get("time"))

    