from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NewType, Optional


Id = NewType("Id", str)


@dataclass(frozen=True)
class User(object):
    id: Id
    username: str
    password: str
    about: str


class Repository(ABC):
    @abstractmethod
    def add(self, a_user: User) -> None:
        pass

    @abstractmethod
    def get_next_id(self) -> Id:
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def find_by_credentials(self, username: str, password: str) -> Optional[User]:
        pass
