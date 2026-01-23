from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class UpdateRequestOutput(BaseModel):
    request : dict
    friendship : Optional[dict] = None

class UpdateRequestInput(BaseModel):
    status : str
    send_user_id : int

class UpdateSentRequestInput(BaseModel):
    status : str
    rec_user_id: int

class RequestByIDInput(BaseModel):
    id: int

class CreateRequest(BaseModel):
    id : int

class RequestOutput(BaseModel):
    id : int
    send_user_id : int
    send_user_name : Optional[str] = None
    rec_user_id : int
    rec_user_name : Optional[str] = None
    status : str
    created : datetime


class RequestsOutput(BaseModel):
    requests : List[RequestOutput]

class BlockedRequestsOutput(BaseModel):
    blocked_requests : List[RequestOutput]