from abc import ABC, abstractmethod

from social_network.entities import post


class Repository(ABC):
    @abstractmethod
    def get_next_id(self) -> post.Id:
        pass

    @abstractmethod
    def add(self, a_post: post.Post) -> None:
        pass
