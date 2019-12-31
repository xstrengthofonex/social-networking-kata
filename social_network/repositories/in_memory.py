from typing import Optional, List
from uuid import uuid4

from social_network.domain import user


class UserRepository(user.Repository):
    def __init__(self):
        self.users: List[user.User] = list()

    def add(self, a_user: user.User) -> None:
        self.users.append(a_user)

    def get_next_id(self) -> user.Id:
        return user.Id(str(uuid4()))

    def username_exists(self, username: str) -> bool:
        return any(u.username == username for u in self.users)

    def find_by_credentials(self, username: str, password: str) -> Optional[user.User]:
        raise NotImplementedError
