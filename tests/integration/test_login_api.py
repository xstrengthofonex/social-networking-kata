import webtest

from tests.integration import dsl


class LoginAPITest(dsl.APITest):
    def setUp(self) -> None:
        super().setUp()
        self.registered_user = self.create_registered_user()

    def test_login_existing_user(self):
        response = self.login(self.registered_user)
        self.assert_user_logged_in(response)

    def test_login_wrong_password_user(self):
        wrong_password_user = dsl.User(username="Username", password="wrongPassword")
        response = self.login(wrong_password_user)
        self.assertEqual("400 Bad Request", response.status)
        self.assertEqual("Invalid Credentials", response.text)

    def login(self, a_user: dsl.User) -> webtest.TestResponse:
        login_credentials = dict(username=a_user.username, password=a_user.password)
        response = self.client.post_json("/login", params=login_credentials, status="*")
        return response

    def assert_user_logged_in(self, response: webtest.TestResponse):
        self.assertEqual("200 OK", response.status)
        self.assertEqual(self.registered_user.id, response.json.get("userId"))
        self.assertEqual(self.registered_user.username, response.json.get("username"))
        self.assertEqual(self.registered_user.about, response.json.get("about"))
