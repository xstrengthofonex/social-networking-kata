from typing import Optional

from social_network.domain import user


class UserRepository(user.Repository):
    def add(self, a_user: user.User) -> None:
        raise NotImplementedError

    def get_next_id(self) -> user.Id:
        raise NotImplementedError

    def username_exists(self, username: str) -> bool:
        raise NotImplementedError

    def find_by_credentials(self, username: str, password: str) -> Optional[user.User]:
        raise NotImplementedError
