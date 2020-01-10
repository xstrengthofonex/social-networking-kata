import webtest

from tests.integration import dsl


class RetrieveTimelineAPITest(dsl.APITest):
    USER = dsl.User()
    TEXT = "Some text"

    def test_return_a_single_post_timeline_for_registered_user(self):
        registered_user = self.create_registered_user()
        created_post = self.create_post(registered_user.id, self.TEXT)
        response = self.retrieve_timeline_for_user(registered_user.id)
        self.assert_timeline(response, created_post)

    def retrieve_timeline_for_user(self, user_id: str) -> webtest.TestResponse:
        return self.client.post_json(f"/users/{user_id}/timeline", status="*")

    def assert_timeline(self, response: webtest.TestResponse, post: dsl.Post) -> None:
        self.assertEqual("200 OK", response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertEqual(post.post_id, response.json[0].get("post_id"))
        self.assertEqual(post.user_id, response.json[0].get("user_id"))
        self.assertEqual(post.text, response.json[0].get("text"))
        self.assertIsNotNone(post.date, response.json[0].get("date"))
        self.assertIsNotNone(post.time, response.json[0].get("time"))
