# User auth & points system added incrementally (no rewrites).
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    name: Optional[str] = "User"

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    name: str
    points: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str
