from tests.integration import dsl


class LoginAPITest(dsl.APITest):
    def test_login_existing_user(self):
        registered_user = self.create_registered_user()
        response = self.login(registered_user)
        self.assert_logged_in_user(registered_user, response)

    def assert_logged_in_user(self, registered_user, response):
        self.assertEqual("200 OK", response.status)
        self.assertEqual(registered_user.id, response.json.get("id"))
        self.assertEqual(registered_user.username, response.json.get("username"))
        self.assertEqual(registered_user.about, response.json.get("about"))

    def login(self, registered_user):
        login_credentials = dict(username=registered_user.username, password=registered_user.password)
        response = self.client.post_json("/login", params=login_credentials)
        return response
