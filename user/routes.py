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
from user.services import create_user_account, user_reset_password
from user.responses import UserResponse, ImageSchema

from core.security import oauth2_scheme
from user.responses import UserResponse
from auth.services import get_token, get_user_by_email, create_access_token, get_all_imgs_details, \
    get_current_user_via_temp_token, get_user_img_by_id
from fastapi import Depends, HTTPException, status, Response
from email_notification.notify import send_reset_password_mail
from user.models import UserModel, ImgsModel
from core.security import create_access_token_forget_password
from fastapi.staticfiles import StaticFiles
from core.config import get_settings
from jose import jwt, JWTError



User = UserModel()
secret_key = get_settings().JWT_SECRET
parent_directory = Path(__file__).parent
templates_path = parent_directory.parent / "templates"
templates = Jinja2Templates(directory=templates_path)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data=data, db=db)
    payload = {"message": "User account has been successfully created."}
    return JSONResponse(content=payload)


@user_router.post('/me' ,status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request, user: User = Depends(oauth2_scheme)):
    print(request.user.idusers)
    return JSONResponse(content=request.user.username)


@router.post("/forgot_password", summary="Trigger forgot password mechanism for a user", tags=["Users"])
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


@router.post('/get_user_mail', status_code=status.HTTP_201_CREATED)
async def get_user_by_emil(request: Request, user_email: str, db: Session = Depends(get_db)):
    users = get_user_by_email(db=db, user_email=user_email)
    return users


@router.get('/get_img_by_id', status_code=status.HTTP_200_OK, response_model=List[ImageSchema])
async def get_all_img_by_id(
        request: Request,
        user: User = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
        page: int = Query(1, gt=0),  # Default page is 1
        per_page: int = Query(10, gt=0),  # Default per_page is 10
        ):
    """
    Get all images for the logged-in user.
    """
    # Decode the JWT token to extract the user ID
    try:
        user_id = request.user.idusers
        print(user_id)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    offset = (page - 1) * per_page

    # user_images = await get_user_img_by_id(db=db, user_id=user_id, offset=offset, limit=per_page)
    user_images = await get_user_img_by_id(db=db, user_id=user_id, offset=offset, limit=per_page)

    base_url = str(request.base_url).rstrip("/static")
    imgs_with_links = [
        {
            "id": img.iduser_img,
            "user_id": img.user_id,
            "img_path": f"{base_url}/static{img.img_path}",
            "pallets_count": img.pallets_count,
            "insert_time": img.insert_time.isoformat(),
            "price_piece": img.price_piece,
            "total_price": img.total_price,
            "transport_fc_count": img.transport_fc_count,
            "co2_saving_count": img.co2_saving_count,
            "total_transport": img.total_transport,
            "co2_fc": img.co2_fc,
            "transport_cost": img.transport_cost,
            "buy_or_sell": img.buy_or_sell

        }
        for img in user_images
    ]

    return JSONResponse(content=imgs_with_links)


@router.post('/get_all_imgs', status_code=status.HTTP_201_CREATED)
async def get_all_imgs(request: Request, user: User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    imgs = get_all_imgs_details(db=db)
    return imgs


@router.post("/reset_password", status_code=status.HTTP_201_CREATED)
def user_reset_password_route(request: Request, new_password: str,
                              user: User = Depends(get_current_user_via_temp_token),
                              db: Session = Depends(get_db)):
    """
    Resets password for a user.
    """
    try:
        result = user_reset_password(db, user.email, new_password)

        print({
            "request": request,
            "success": result
        })

    except Exception as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        logger.error(f'From {request.endpoint} {msg}', exc_info=e)

