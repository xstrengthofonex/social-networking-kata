from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import uuid4

from social_network.entities import user


class Repository(ABC):
    @abstractmethod
    def add(self, a_user: user.User) -> None:
        pass

    @abstractmethod
    def get_next_id(self) -> user.Id:
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def find_by_credentials(self, username: str, password: str) -> Optional[user.User]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: user.Id) -> Optional[user.User]:
        pass
    
    @abstractmethod
    def add_follower(self, follower_id: user.Id, followee_id: user.Id) -> None:
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self.users: List[user.User] = list()

    def add(self, a_user: user.User) -> None:
        self.users.append(a_user)

    def get_next_id(self) -> user.Id:
        return user.Id(str(uuid4()))

    def username_exists(self, username: str) -> bool:
        return any(u.username == username for u in self.users)

    def find_by_credentials(self, username: str, password: str) -> Optional[user.User]:
        return next((u for u in self.users if u.has_credentials(username, password)), None)

    def find_by_id(self, user_id: user.Id) -> Optional[user.User]:
        return next((u for u in self.users if u.id == user_id), None)

    def add_follower(self, follower_id: user.Id, followee_id: user.Id) -> None:
        # not needed yet
        pass