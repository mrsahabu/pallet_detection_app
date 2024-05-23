from pydantic import BaseModel, EmailStr
#demo code

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class changepassword(BaseModel):
    email: str
    old_password: str
    new_password: str