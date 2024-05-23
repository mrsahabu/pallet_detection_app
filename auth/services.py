import sys

from core.security import verify_password
from core.config import get_settings
from auth.responses import TokenResponse
from core.security import create_access_token, create_refresh_token, get_token_payload
from fastapi import Depends, HTTPException, status
from user.models import UserModel, ImgsModel
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

User = UserModel()
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


async def _get_user_token(user: UserModel, refresh_token=None):
    payload = {"id": user.idusers}

    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds  # in seconds
    )


# async def _get_user_token(user: UserModel, refresh_token=None):
#     payload = {"id": user.idusers}
#
#     access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#
#     access_token = await create_access_token(payload, access_token_expiry)
#     if not refresh_token:
#         refresh_token = await create_refresh_token(payload)
#     return TokenResponse(
#         access_token=access_token,
#         refresh_token=refresh_token,
#         expires_in=access_token_expiry.seconds  # in seconds
#     )


def get_user_by_email(db: Session, user_email: str):
    user = db.query(UserModel).filter(UserModel.email == user_email).first()
    return user


# def create_access_token(data: str, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
#     to_encode = {"sub": data}
#     expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


def get_user_img_by_id(db: Session, user_id: int, offset: int, limit: int):
    query = db.query(ImgsModel).filter(ImgsModel.user_id == user_id)
    query = query.offset(offset).limit(limit)
    user_videos = query.all()

    return user_videos


def get_all_imgs_details(db: Session):
    user_imgs = db.query(ImgsModel).all()

    return user_imgs


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
        print(msg, '******************************************')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT Token could not be validated",
            headers={"WWW-Authenticate": "Bearer"}
        )


# def get_token_payload(token: str = Depends(oauth2_scheme)):
#
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         payload_sub: str = payload.get("sub")
#         if payload_sub is None:
#             raise BearAuthException("Token could not be validated")
#         return payload_sub
#     except JWTError:
#         raise BearAuthException("Token could not be validated")


def get_current_user_via_temp_token(access_token: str, db: Session = Depends(get_db)):
    try:
        user_email = get_token_payload(access_token)
        print("******", user_email, "**********")
    except BearAuthException as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        user = db.query(User).filter(User.email == user_email).first()
    except Exception as e:
        # print(f"DB Query Error: {e}")
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        print("******", msg)
        raise

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found, could not find User.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
