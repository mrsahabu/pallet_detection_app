import sys
from pathlib import Path
from venv import logger

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from core.database import get_db
from user.schemas import CreateUserRequest
from user.services import create_user_account, user_reset_password

from core.security import oauth2_scheme
from user.responses import UserResponse
from auth.services import get_token, get_user_by_email, create_access_token, get_user_videos, \
    get_current_user_via_temp_token
from fastapi import Depends, HTTPException, status
from email_notification.notify import send_reset_password_mail
from user.models import UserModel
from core.security import create_access_token_forget_password

User = UserModel()

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


@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    print(request.user.username)
    return request.user


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
            # Update this line to use 'expiry' instead of 'expire_minutes'
            access_token = await create_access_token_forget_password(data={"email": user.email},
                                                                     expiry=TEMP_TOKEN_EXPIRE_MINUTES * 60)
            url = f"{request.base_url}reset_password_template?access_token={access_token}"
            await send_reset_password_mail(recipient_email=user.email, user=user, url=url,
                                           expire_in_minutes=TEMP_TOKEN_EXPIRE_MINUTES)
        return {
            "result": f"An email has been sent to {user.email} with a link for password reset."
        }
    except Exception as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        logger.error(f'From {request.endpoint} {msg}', exc_info=e)


@router.post('/get_user_mail', status_code=status.HTTP_201_CREATED)
async def get_user_by_emil(request: Request, user_email: str, db: Session = Depends(get_db)):
    users = get_user_by_email(db=db, user_email=user_email)
    return users


@router.post('/get_all_videos_details', status_code=status.HTTP_201_CREATED)
async def get_all_videos(request: Request, db: Session = Depends(get_db)):
    vids = get_user_videos(db=db)
    return vids


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
