from pydantic import BaseModel, EmailStr


class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    idusers: int
    username: str
    email: EmailStr
    img_path: str
