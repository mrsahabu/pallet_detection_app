from user.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from sqlalchemy.orm import Session
from user.models import UserModel
from auth.services import get_user_by_email
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user_account(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")

    new_user = UserModel(
        username=data.username,
        email=data.email,
        role=data.role,
        password=get_password_hash(data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def reset_password(db: Session, email: str, new_password: str):
    user = get_user_by_email(db, email)
    if user:
        user.password = pwd_context.hash(new_password)
        db.commit()
        return True
    return False
