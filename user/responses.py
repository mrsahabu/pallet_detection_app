from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime
from typing import List, Optional

#demo code
class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    idusers: int
    username: str
    email: EmailStr


class ImageSchema(BaseModel):
    id: int
    user_id: int
    img_path: str
    pallets_count: Optional[int]
    insert_time: datetime

    class Config:
        from_attributes = True
