from itertools import zip_longest
from typing import List

import webtest

from tests.integration import dsl


class RetrieveWallAPITest(dsl.APITest):
    def test_retrieves_wall_of_user_posts_and_followee_posts_in_reverse_order(self):
        user_1 = self.create_registered_user("User1")
        user_2 = self.create_registered_user("User2")
        user_3 = self.create_registered_user("User3")
        self.create_following(user_1.id, user_2.id)
        self.create_following(user_1.id, user_3.id)
        post_1 = self.create_post(user_1.id, "Post 1")
        post_2 = self.create_post(user_2.id, "Post 2")
        post_3 = self.create_post(user_3.id, "Post 3")
        post_4 = self.create_post(user_1.id, "Post 4")

        response = self.retrieve_wall(user_1.id)

        self.assertEqual("200 OK", response.status)
        self.assert_wall(response.json, [post_4, post_3, post_2, post_1])

    def retrieve_wall(self, user_id: str) -> webtest.TestResponse:
        return self.client.get(f"/users/{user_id}/wall", status="*")

    def assert_wall(self, actual_posts: List[dict], expected_posts: List[dsl.Post]) -> None:
        for (expected_post, actual_post) in zip_longest(expected_posts, actual_posts, fillvalue=dict()):
            self.assertEqual(expected_post.post_id, actual_post.get("postId"))
            self.assertEqual(expected_post.user_id, actual_post.get("userId"))
            self.assertEqual(expected_post.text, actual_post.get("text"))
            self.assertEqual(expected_post.time, actual_post.get("time"))
            self.assertEqual(expected_post.date, actual_post.get("date"))

