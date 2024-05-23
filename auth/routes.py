from typing import Dict

from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from core.database import get_db
from auth.services import get_token, get_refresh_token, oauth2_scheme
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)
token_store: Dict[str, str] = {}



@router.post("/token", status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    if token in token_store:
        del token_store[token]
    return {"message": "Successfully logged out"}


# @router.get('/logout', status_code=status.HTTP_200_OK)
# def logout(response: Response, Authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):
#     Authorize.unset_jwt_cookies()
#     response.delete_cookie('logged_in')
#     return {"message": "Successfully logged out"}
