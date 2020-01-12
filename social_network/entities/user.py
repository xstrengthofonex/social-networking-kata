from dataclasses import dataclass
from typing import NewType, NamedTuple

Id = NewType("Id", str)


@dataclass(frozen=True)
class User(object):
    id: Id
    username: str
    password: str
    about: str

    def has_credentials(self, username: str, password: str) -> bool:
        return self.username == username and self.password == password


FollowerId = NewType("FollowerId", user.Id)
FolloweeId = NewType("FolloweeId", user.Id)
Following = NamedTuple("Following", [("follower_id", FollowerId), ("followee_id", FolloweeId)])