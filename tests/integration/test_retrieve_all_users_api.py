from typing import List, Dict

import webtest

from tests.integration import dsl


class RetrieveAllUsersAPITest(dsl.APITest):
    def test_retrieving_all_users(self):
        user_1 = self.create_registered_user("Avi")
        user_2 = self.create_registered_user("Vince")

        response = self.retrieve_all_users()

        self.assert_retrieved_all_users(response, [user_1, user_2])

    def retrieve_all_users(self) -> webtest.TestResponse:
        return self.client.get("/users", status="*")

    def assert_retrieved_all_users(self, response, expected_users):
        self.assertEqual("200 OK", response.status)
        self.assertEqual("application/json", response.content_type)
        self.assertListEqual(self.json_users_to_dsl_users(response.json),
                             expected_users)

    @staticmethod
    def json_user_to_dsl_user(json_user: Dict[str, str]) -> dsl.User:
        return dsl.User(
            id=json_user.get("id"),
            username=json_user.get("username"),
            about=json_user.get("about"))

    def json_users_to_dsl_users(self, json_users: List[Dict[str, str]]) -> List[dsl.User]:
        return [self.json_user_to_dsl_user(u) for u in json_users]
