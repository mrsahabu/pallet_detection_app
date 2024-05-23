from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class changepassword(BaseModel):
    email: str
    old_password: str
    new_password: str