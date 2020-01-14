from typing import List

import webtest

from tests.integration import dsl


class FollowUserAPITest(dsl.APITest):
    def test_retrieve_followees_for_a_registered_user(self):
        user = self.create_registered_user("User")
        followee_a = self.create_registered_user("Followee A")
        followee_b = self.create_registered_user("Followee B")
        self.create_following(user.id, followee_a.id)
        self.create_following(user.id, followee_b.id)

        response = self.retrieve_followees(user.id)

        expected_followees = [followee_a, followee_b]
        self.assert_following(response, expected_followees)

    def retrieve_followees(self, user_id: str) -> webtest.TestResponse:
        follow_request_data = dict(user_id=user_id)
        return self.client.get(f"/users/{user_id}/followees", params=follow_request_data, status="*")

    def assert_following(self, response: webtest.TestResponse, expected_followees: List[dsl.User]) -> None:
        self.assertEqual("200 OK", response.status)
        self.assertEqual(expected_followees, self.json_users_to_dsl_users(response.json))
