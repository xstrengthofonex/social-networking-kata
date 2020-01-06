from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import uuid4
from social_network.entities import post


class Repository(ABC):
    @abstractmethod
    def get_next_id(self) -> post.Id:
        pass

    @abstractmethod
    def add(self, a_post: post.Post) -> None:
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self.posts: List[post.Post] = list()

    def add(self, a_post: post.Post) -> None:
        self.posts.append(a_post)

    def get_next_id(self) -> post.Id:
        return post.Id(str(uuid4()))