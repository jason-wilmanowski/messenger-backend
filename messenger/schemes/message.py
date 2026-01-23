from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ConversationMessageInput(BaseModel):
    conversation_id: int

class MessageCreate(BaseModel):
    conversation_id : int
    body : str

class MessageUpdateDetails(BaseModel):
    id : int
    body : str

class MessageDeleteDetails(BaseModel):
    id : int

class MessageOutput(BaseModel):
    id : int
    conversation_id : int
    user_id : int
    body : str
    created : datetime
    updated : Optional[datetime] = None

class MessagesOutput(BaseModel):
    messages : List[MessageOutput]


    class Config:
        from_attributes = True
