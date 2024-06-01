import sys

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from core.security import verify_password
from core.config import get_settings
from auth.responses import TokenResponse
from core.security import create_access_token, create_refresh_token, get_token_payload
from fastapi import Depends, HTTPException, status
from user.models import UserModel, FileModel, DataModel
# from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, session
from core.database import get_db


class BearAuthException(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

User = UserModel()
img_model = DataModel()
settings = get_settings()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM


async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_token(user=user)


async def get_refresh_token(token, db):
    payload = get_token_payload(token=token)
    user_id = payload.get('id', None)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_user_token(user=user, refresh_token=token)


async def get_user_by_token(token: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.idusers == token))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


async def _get_user_token(user: UserModel, refresh_token=None):
    payload = {"id": user.id}

    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds  # in seconds
    )

def get_user_data_by_email(db: Session, email: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    return user



async def get_user_img_by_id(db: AsyncSession, user_id: int, offset: int, limit: int):
    # result = DataModel.query.filter(DataModel.user_id==user_id).offset(offset).limit(limit).all()
    query = select(DataModel).where(DataModel.user_id == user_id).offset(offset).limit(limit)
    result = db.execute(query)
    user_images = result.scalars().all()
    return user_images


# async def get_user_img_by_id(db: AsyncSession, user_id: int, offset: int, limit: int):
#     query = select(DataModel).where(img_model.user_id == user_id).offset(offset).limit(limit)
#     result = await db.execute(query)
#     user_images = result.scalars().all()
#     for img in user_images:
#         yield img


def get_token_payload(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        payload_sub: str = payload.get("email")
        print("***********", payload)
        if payload_sub is None:
            raise BearAuthException("Payload could not be validated")
        return payload_sub
    except JWTError as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT Token could not be validated",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user_via_temp_token(access_token: str, db: Session = Depends(get_db)):
    try:
        user_email = get_token_payload(access_token)
    except BearAuthException as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        user = db.query(UserModel).filter(UserModel.email == user_email).first()

    except Exception as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        raise

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found, could not find User.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
