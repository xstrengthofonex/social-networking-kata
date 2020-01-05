from dataclasses import dataclass
from typing import NewType

Id = NewType("Id", str)


@dataclass(frozen=True)
class User(object):
    id: Id
    username: str
    password: str
    about: str

    def has_credentials(self, username: str, password: str) -> bool:
        return self.username == username and self.password == password
