from tests.integration import dsl


class RegisterUserAPITest(dsl.APITest):
    ALICE = dsl.User(username="Alice", password="123456", about="About Alice")

    def test_register_user(self):
        registration_data = dict(
            username=self.ALICE.username,
            password=self.ALICE.password,
            about=self.ALICE.about)

        response = self.client.post_json("/registration", params=registration_data)

        self.assertEqual(201, response.status_int)
        self.assertEqual("201 - CREATED", response.status)
        self.assertIsNotNone(response.json.get("id"))
        self.assertEqual(self.ALICE.username, response.json.get("username"))
        self.assertEqual(self.ALICE.about, response.json.get("about"))

    def test_attempt_register_user_with_existing_user(self):
        registration_data = dict(
            username=self.ALICE.username,
            password=self.ALICE.password,
            about=self.ALICE.about)
        self.client.post_json("/registration", params=registration_data)

        response = self.client.post_json("/registration", params=registration_data)

        self.assertEqual(400, response.status_int)
        self.assertEqual("400 - BAD_REQUEST", response.status)
        self.assertEqual("Username already in use", response.json)
        