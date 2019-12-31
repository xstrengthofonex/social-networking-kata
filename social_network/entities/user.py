from dataclasses import dataclass
from typing import NewType

Id = NewType("Id", str)


@dataclass(frozen=True)
class User(object):
    id: Id
    username: str
    password: str
    about: str
