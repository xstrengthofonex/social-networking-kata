from tests.integration import dsl


class RegisterUserAPITest(dsl.APITest):
    ALICE = dsl.User(username="Alice", password="123456", about="About Alice")

    def test_register_user(self):
        registration_data = dict(
            username=self.ALICE.username,
            password=self.ALICE.password,
            about=self.ALICE.about)

        response = self.client.post_json("/registration", params=registration_data)

        self.assertEqual("201 Created", response.status)
        self.assertIsNotNone(response.json.get("userId"))
        self.assertEqual(self.ALICE.username, response.json.get("username"))
        self.assertEqual(self.ALICE.about, response.json.get("about"))

    def test_attempt_register_user_with_existing_user(self):
        registration_data = dict(
            username=self.ALICE.username,
            password=self.ALICE.password,
            about=self.ALICE.about)
        self.client.post_json("/registration", params=registration_data)

        response = self.client.post_json("/registration", params=registration_data, status="400 Bad Request")

        self.assertEqual("Username already in use", response.text)
