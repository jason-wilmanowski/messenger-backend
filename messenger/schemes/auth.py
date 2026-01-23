from pydantic import BaseModel


class Payload(BaseModel):
    sub : str
    exp : int
    iat : int

class TokenOutput(BaseModel):
    access_token : str
    token_type : str
    user_id : int