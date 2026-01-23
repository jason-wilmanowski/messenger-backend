from pydantic import BaseModel
from datetime import datetime
from typing import List



class UserConversation(BaseModel):
    user_id: int

class ConversationCreate(BaseModel):
    user_id_1 : int
    user_id_2 : int

class ConversationCreateOrGet(BaseModel):
    user_id_2 : int

class ConversationOutput(ConversationCreate):
    id : int
    created : datetime

class UserConversationsOutput(BaseModel):
    conversations: List[ConversationOutput]