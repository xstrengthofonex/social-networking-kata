from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NewType


Id = NewType("Id", str)


@dataclass(frozen=True)
class User(object):
    id: Id
    username: str
    password: str
    about: str


class Repository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        True

    @abstractmethod
    def get_next_id(self) -> Id:
        pass
