from user.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from sqlalchemy.orm import Session
from user.models import UserModel
#demo code 

async def create_user_account(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")

    new_user = UserModel(
        username=data.username,
        email=data.email,
        password=get_password_hash(data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def user_reset_password(db: Session, email: str, new_password: str):
    try:
        user = db.query(UserModel).filter(UserModel.email == email)
        user.password = get_password_hash(new_password)
        # db.add(user)
        db.commit()

    except Exception as e:
        raise (e)
        return False
    return True
