from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, Float


class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

