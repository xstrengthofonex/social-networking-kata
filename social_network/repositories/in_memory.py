from typing import Optional

from social_network.domain import user


class UserRepository(user.Repository):
    users = []
    def add(self, a_user: user.User) -> None:
       self.users.append(a_user)

    def get_next_id(self) -> user.Id:
        return user.Id(len(self.users) + 1)

    def username_exists(self, username: str) -> bool:
        any(user.username == username for user in self.users) 

    def find_by_credentials(self, username: str, password: str) -> Optional[user.User]:
        raise NotImplementedError
