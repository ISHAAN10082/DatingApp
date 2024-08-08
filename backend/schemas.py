from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    uid: str
    email: str
    first_name: str
    last_name: str
    gender: str
    latitude: float
    longitude: float

class User(UserBase):
    #id: int
    run_id: str
    run_iteration: int
    datetime: datetime

    class Config:
        orm_mode = True

class Message(BaseModel):
    message: str
    run_id: str