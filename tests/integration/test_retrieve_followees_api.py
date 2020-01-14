import webtest

from tests.integration import dsl


class FollowUserAPITest(dsl.APITest):
    def test_retreieve_followees_for_a_registered_user(self):
        user = self.create_registered_user("User")
        followee_a = self.create_registered_user("Followee A")
        followee_b = self.create_registered_user("Followee B")
        self.create_following(user.id, followee_a.id)
        self.create_following(user.id, followee_b.id)
        response = self.retreive_followees(user.id)
        expected_followees = [self.make_user_dto(followee_a), self.make_user_dto(followee_b)]
        self.assert_following(response, expected_followees)

    def retreive_followees(self, user_id: str) -> webtest.TestResponse:
        follow_request_data = dict(user_id=user_id)
        return self.client.post_json("/users/${user_id}/followees", params=follow_request_data, status="*")

    def assert_following(self, response: webtest.TestResponse, expected_followees) -> None:
        self.assertEqual("201 Created", response.status)
        self.assertEqual(expected_followees, response.json.get("followees"))
