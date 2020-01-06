import webtest

from tests.integration import dsl


class CreatePostAPITest(dsl.APITest):
    USER = dsl.User()
    TEXT = "Some text"

    def test_create_a_new_post_with_a_registered_user(self):
        # There seem to be no checks that a user is logged in
        # I think they decided to forgo sessions and authorization in the requirements

        registered_user = self.create_registered_user()
        response = self.create_post(registered_user.id, self.TEXT)
        self.assert_post_created(response, registered_user.id, self.TEXT)

    def create_post(self, user_id: str, text: str) -> webtest.TestResponse:
        create_post_data = dict(user_id=user_id, text=text)
        return self.client.post_json("/users/{user_id}/posts", params=create_post_data, status="*")

    def assert_post_created(self, response: webtest.TestResponse, user_id: str, text: str) -> None:
        self.assertEqual("201 Created", response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertIsNotNone(response.json.get("post_id"))
        self.assertEqual(user_id, response.json.get("user_id"))
        self.assertEqual(text, response.json.get("text"))
        self.assertIsNotNone(response.json.get("date"))
        self.assertIsNotNone(response.json.get("time"))

    def test_do_not_create_a_new_post_with_a_missing_user(self):
        # There seem to be no checks that a user is logged in
        # I think they decided to forgo sessions and authorization in the requirements

        response = self.create_post(None, self.TEXT)
        self.assert_post_not_created(response)
        
    def assert_post_not_created(self, response: webtest.TestResponse) -> None:
        self.assertEqual("400 Bad Request", response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertEqual("User Does Not Exist.", response.text)
