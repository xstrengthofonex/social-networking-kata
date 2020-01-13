from abc import ABC, abstractmethod
from typing import List
from uuid import uuid4

from social_network.posts import post
from social_network.users import user


class Repository(ABC):
    @abstractmethod
    def get_next_id(self) -> post.Id:
        pass

    @abstractmethod
    def add(self, a_post: post.Post) -> None:
        pass

    @abstractmethod
    def get_timeline_for_user(self, user_id: user.Id) -> List[post.Post]:
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self.posts: List[post.Post] = list()

    def add(self, a_post: post.Post) -> None:
        self.posts.append(a_post)

    def get_next_id(self) -> post.Id:
        return post.Id(str(uuid4()))

    def get_timeline_for_user(self, user_id: user.Id) -> List[post.Post]:
        return [p for p in self.posts if p.user_id == user.Id(user_id)]
