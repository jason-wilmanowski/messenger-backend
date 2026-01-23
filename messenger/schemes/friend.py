from pydantic import BaseModel
from typing import List
from datetime import datetime


class FriendsItem(BaseModel):
    username : str
    id : int

class FriendsOutput(BaseModel):
    friends : List[FriendsItem]

class FriendshipOutput(BaseModel):
    id : int
    user_id_1 : int
    user_id_2 : int
    created : datetime