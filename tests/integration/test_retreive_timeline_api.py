from typing import List

import webtest

from tests.integration import dsl


class RetrieveTimelineAPITest(dsl.APITest):
    def test_returns_a_timeline_for_registered_user_in_reverse_chronological_order(self):
        registered_user = self.create_registered_user()
        post_1 = self.create_post(registered_user.id, "Post 1")
        post_2 = self.create_post(registered_user.id, "Post 2")
        response = self.retrieve_timeline_for_user(registered_user.id)
        self.assert_timeline(response, [post_2, post_1])

    def test_returns_error_if_user_does_not_exist(self):
        response = self.retrieve_timeline_for_user("NonExistentUser")
        self.assert_user_does_not_exist(response)

    def retrieve_timeline_for_user(self, user_id: str) -> webtest.TestResponse:
        return self.client.get(f"/users/{user_id}/timeline", status="*")

    def assert_timeline(self, response: webtest.TestResponse, posts: List[dsl.Post]) -> None:
        self.assertEqual("200 OK", response.status)
        self.assertEqual("application/json", response.content_type)
        for expected, result in zip(posts, response.json):
            self.assertEqual(expected.post_id, result.get("postId"))
            self.assertEqual(expected.user_id, result.get("userId"))
            self.assertEqual(expected.text, result.get("text"))
            self.assertIsNotNone(expected.date, result.get("date"))
            self.assertIsNotNone(expected.time, result.get("time"))

    def assert_user_does_not_exist(self, response: webtest.TestResponse) -> None:
        self.assertEqual("400 Bad Request", response.status)
        self.assertEqual("text/plain", response.content_type)
        self.assertEqual("User does not exist.", response.text)
