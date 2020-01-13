from dataclasses import dataclass
from datetime import datetime

from social_network.posts import post
from social_network.users import user


@dataclass(frozen=True)
class Post(object):
    id: post.Id
    user_id: user.Id
    text: str
    created_on: datetime
