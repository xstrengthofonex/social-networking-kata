from tests.integration import dsl


class RegisterUserAPITest(dsl.APITest):
    ALICE = dsl.User(username="Alice", password="123456", about="About Alice")

    def test_register_user(self):
        registration_data = dict(
            username=self.ALICE.username,
            password=self.ALICE.password,
            about=self.ALICE.about)

        response = self.client.post_json("/registration", params=registration_data)

        self.assertEqual(200, response.status_int)
        self.assertIsNotNone(response.json.get("id"))
        self.assertEqual(self.ALICE.username, response.json.get("username"))
        self.assertEqual(self.ALICE.about, response.json.get("about"))
