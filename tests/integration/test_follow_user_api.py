import webtest

from tests.integration import dsl


class FollowUserAPITest(dsl.APITest):
    def test_a_registered_user_can_follow_another_registered_user(self):
        follower = self.create_registered_user("Follower")
        followee = self.create_registered_user("Followee")
        response = self.follow_user(follower.id, followee.id)
        self.assert_following(response)

    def test_cannot_create_following_if_one_of_the_users_is_not_registered(self):
        follower = self.create_registered_user("Follower")
        response = self.follow_user(follower.id, "NonExistentFollowee")
        self.assert_no_following(response)

    def follow_user(self, follower_id: str, followee_id: str) -> webtest.TestResponse:
        follow_request_data = dict(followerId=follower_id, followeeId=followee_id)
        return self.client.post_json("/follow", params=follow_request_data, status="*")

    def assert_following(self, response: webtest.TestResponse) -> None:
        self.assertEqual("201 Created", response.status)

    def assert_no_following(self, response: webtest.TestResponse) -> None:
        self.assertEqual("400 Bad Request", response.status)
        self.assertEqual("text/plain", response.content_type)
        self.assertEqual("At least one of the users does not exist.", response.text)
