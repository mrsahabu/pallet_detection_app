import base64
import os
import sys
from pathlib import Path
from typing import List
from venv import logger

from fastapi import APIRouter, Request, Query, Header
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates

from core.database import get_db, settings
from user.schemas import CreateUserRequest
from user.services import create_user_account, reset_password
from user.responses import UserResponse

from core.security import oauth2_scheme
from user.responses import UserResponse
from auth.services import get_user_by_email, get_current_user_via_temp_token
from fastapi import Depends, HTTPException, status, Response
from email_notification.notify import send_reset_password_mail
from user.models import UserModel, DataModel, FileModel
from core.security import create_access_token_forget_password
from fastapi.staticfiles import StaticFiles
from core.config import get_settings
from jose import jwt, JWTError



User = UserModel()
secret_key = get_settings().JWT_SECRET
parent_directory = Path(__file__).parent
templates_path = parent_directory.parent / "templates"
templates = Jinja2Templates(directory=templates_path)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@user_router.post('/create-user', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data=data, db=db)
    payload = {"message": "User account has been successfully created."}
    return JSONResponse(content=payload,status_code=status.HTTP_201_CREATED)


@user_router.get('/me' ,status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request, user: User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = db.query(UserModel).filter_by(id=request.user.id).first()

    
    data = {
        "id": user_data.id,
        "username": user_data.username,
        "email": user_data.email,
        "role": user_data.role
        }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@user_router.post("/forgot_password", summary="Trigger forgot password mechanism for a user", tags=["Users"])
async def user_forgot_password(request: Request, user_email: str, db: Session = Depends(get_db)):
    """
    Triggers forgot password mechanism for a user.
    """
    msg = 'User does not exist'
    TEMP_TOKEN_EXPIRE_MINUTES = 10
    try:
        user = get_user_by_email(db=db, user_email=user_email)
        if user:
            access_token = await create_access_token_forget_password(data={"email": user.email},
                                                                     expiry=TEMP_TOKEN_EXPIRE_MINUTES * 60)
            url = f"{request.base_url}reset_password?access_token={access_token}"
            await send_reset_password_mail(recipient_email=user.email, user=user, url=url,
                                           expire_in_minutes=TEMP_TOKEN_EXPIRE_MINUTES)
        return {
            "result": f"An email has been sent to  with a link for password reset."
        }
    except Exception as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        logger.error(f'From {request.endpoint} {msg}', exc_info=e)


@user_router.post("/reset_password", status_code=status.HTTP_201_CREATED)
async def reset_password_route(
    new_password: str,
    user: UserModel = Depends(get_current_user_via_temp_token),
    access_token: str = Query(),
    db: Session = Depends(get_db)
):
    try:
        reset_password(db, user.email, new_password)
        return {"message": "Password reset successful"}
    except Exception as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

