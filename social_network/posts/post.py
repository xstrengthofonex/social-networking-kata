from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from social_network.users import user


Id = NewType("Id", str)


@dataclass(frozen=True)
class Post(object):
    id: Id
    user_id: user.Id
    text: str
    created_on: datetime
