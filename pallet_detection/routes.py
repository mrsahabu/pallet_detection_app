from aiosmtplib import status
from fastapi.security import HTTPBasic
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core.database import get_db

from fastapi import Depends, FastAPI
from venv import logger

from fastapi import APIRouter, Request, UploadFile
from .utils import img_pred
from .services import insert_img
from fastapi import APIRouter
from PIL import Image
from io import BytesIO
import sys
from urllib import request
from datetime import datetime
from fastapi import HTTPException, status
from user.responses import UserResponse
from core.security import oauth2_scheme
from user.models import UserModel
from email_notification.notify import send_email_with_images_and_count


router = APIRouter(
    prefix="/pallet_detection",
    tags=["yolo-detection"],
    responses={404: {"description": "Not found"}},
)

User = UserModel()

pallet_detection_router = APIRouter(
    prefix="/pallet_detection",
    tags=["pallet detection system"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/image_upload", summary="Get pallets count")
async def upload_img(request: Request, email_to: str,
                     files: list[UploadFile],
                     user: User = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)
                     ):
    """
    Upload images and return predictions.
    """
    user_id = request.user.idusers
    user_name = request.user.username
    pallets_count = 0
    detect_rest = None
    insert_time = datetime.now()
    folder_name = f'/home/cyber-makarov/pallet_fast/uploaded_imgs/{user_name}'
    image_paths = []

    try:
        for img_file in files:
            contents = await img_file.read()
            input_img = Image.open(BytesIO(contents))
            pallets_count, detect_rest, full_img_path = img_pred(input_img, folder_name, img_file.filename)
            image_paths.append(full_img_path)

            success = await insert_img(db, full_img_path, user_id, pallets_count, insert_time)

            if not success:
                raise HTTPException(status_code=500, detail="Failed to insert data into database")

        # Send email with images and pallets count
        email_to = email_to
        subject = "Pallets Count Report"
        message = "Attached are the images uploaded and their corresponding pallets count."
        send_email_with_images_and_count(email_to, subject, message, image_paths, pallets_count)

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Images uploaded and email sent successfully."})

    except Exception as e:
        # Log the error
        print(f"Error during image upload: {e}")
        # Return an error response
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "An error occurred during image upload."})


