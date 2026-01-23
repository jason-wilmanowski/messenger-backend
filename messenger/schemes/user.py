from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict



class UserCreate(BaseModel):
    name: str
    password: str
    email: str

class UserOutput(BaseModel):
    name : str
    email : str
    id : int
    status : str
    created : datetime

    model_config = ConfigDict(from_attributes=True)


class UsersOutput(BaseModel):
    users : List[UserOutput]

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name : Optional[str] = None
    email : Optional[str] = None

class UserPasswordUpdate(BaseModel):
    password : str
    new_password : str


class UserLogin(BaseModel):
    email: str
    password: str

class UserInternal(BaseModel):
    id : int
    name: str
    email: str
    password: str
    status: str
    created : datetime
