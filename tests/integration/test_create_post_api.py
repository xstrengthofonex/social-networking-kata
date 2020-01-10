import webtest

from tests.integration import dsl


class CreatePostAPITest(dsl.APITest):
    USER = dsl.User()
    TEXT = "Some text"

    def test_create_a_new_post_with_a_registered_user(self):
        registered_user = self.create_registered_user()
        response = self.create_post(registered_user.id, self.TEXT)
        self.assert_post_created(response, registered_user.id, self.TEXT)

    def test_do_not_create_a_new_post_with_a_missing_user(self):
        response = self.create_post("unregisteredUser", self.TEXT)
        self.assert_post_not_created(response)

    def create_post(self, user_id: str, text: str) -> webtest.TestResponse:
        create_post_data = dict(text=text)
        return self.client.post_json(f"/users/{user_id}/posts", params=create_post_data, status="*")

    def assert_post_created(self, response: webtest.TestResponse, user_id: str, text: str) -> None:
        self.assertEqual("201 Created", response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertIsNotNone(response.json.get("postId"))
        self.assertEqual(user_id, response.json.get("userId"))
        self.assertEqual(text, response.json.get("text"))
        self.assertIsNotNone(response.json.get("date"))
        self.assertIsNotNone(response.json.get("time"))

    def assert_post_not_created(self, response: webtest.TestResponse) -> None:
        self.assertEqual("400 Bad Request", response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertEqual("User Does Not Exist.", response.text)
