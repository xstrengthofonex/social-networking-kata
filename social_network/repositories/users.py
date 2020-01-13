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

    @abstractmethod
    def find_followees_for(self, follower_id: user.Id) -> List[user.User]:
        pass

    @abstractmethod
    def find_followers_for(self, followee_id: user.Id) -> List[user.User]:
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[user.User]:
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self.users: List[user.User] = list()
        self.followings: List[user.Following] = list()

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
        self.followings.append(user.Following(
            user.FollowerId(follower_id), user.FolloweeId(followee_id)))

    def find_followers_for(self, followee_id: user.Id) -> List[user.User]:
        return [self.find_by_id(u.follower_id)
                for u in self.followings
                if u.followee_id == followee_id]

    def find_followees_for(self, follower_id: user.Id) -> List[user.User]:
        return [self.find_by_id(u.followee_id)
                for u in self.followings
                if u.follower_id == follower_id]
    
    def get_all_users(self) -> List[user.User]:
        return self.users
    