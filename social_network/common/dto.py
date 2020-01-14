from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Post(object):
    id: str
    user_id: str
    text: str
    created_on: datetime


@dataclass(frozen=True)
class User(object):
    id: str
    username: str
    about: str
