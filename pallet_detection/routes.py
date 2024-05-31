from typing import List

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
async def upload_img(
        request: Request,
        email_to: str,
        files: List[UploadFile],
        buy_or_sell: str,
        user: User = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Upload images and return predictions.
    """
    user_id = request.user.idusers
    user_name = request.user.username
    pallets_count = 0
    insert_time = datetime.now()
    folder_name = f'static/{user_name}'
    image_paths = []

    try:
        for img_file in files:
            contents = await img_file.read()
            input_img = Image.open(BytesIO(contents))
            pallets_count, full_img_path = img_pred(input_img, folder_name, img_file.filename)
            image_paths.append(full_img_path)

            # Calculate additional data
            price_piece = 41
            transport_fc = 0.015
            co2_fc = 34.77
            transport_cost = 700
            transport_fc_count = pallets_count * transport_fc if buy_or_sell == "buy" else 0
            total_transport = transport_fc_count * transport_cost if buy_or_sell == "buy" else 0
            total_price = pallets_count * price_piece
            co2_saving_count = transport_fc_count * co2_fc

            # Insert image data into the database
            success = await insert_img(
                db,
                full_img_path,
                user_id,
                pallets_count,
                insert_time,
                price_piece,
                total_price,
                transport_fc_count,
                co2_saving_count,
                total_transport,
                co2_fc,
                transport_cost,
                buy_or_sell
            )

            if not success:
                raise HTTPException(status_code=500, detail="Failed to insert data into database")

        # Send email with images and pallets count
        subject = "Pallets Count Report"
        message = "Attached are the images uploaded and their corresponding pallets count."
        send_email_with_images_and_count(email_to, subject, message, image_paths, pallets_count)

        # Return JSON response with calculated data
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Images uploaded and email sent successfully.",
            "pallets_count": pallets_count,
            "price_piece": price_piece,
            "total_price": total_price,
            "transport_fc_count": transport_fc_count,
            "co2_saving_count": co2_saving_count,
            "total_transport": total_transport,
            "co2_fc": co2_fc,
            "transport_cost": transport_cost,
            "buy_or_sell": buy_or_sell
        })

    except Exception as e:
        # Log the error
        print(f"Error during image upload: {e}")
        msg = f"Error [{str(e)}] at line [{sys.exc_info()[2].tb_lineno}]"
        logger.error(f'From {request.endpoint} {msg}', exc_info=e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
            "message": "An error occurred during image upload."
        })

# @router.post("/image_upload", summary="Get pallets count")
# async def upload_img(
#         request: Request,
#         email_to: str,
#         files: List[UploadFile],
#         buy_or_sell: str,  # Add this parameter
#         user: User = Depends(oauth2_scheme),
#         db: Session = Depends(get_db)
# ):
#     """
#     Upload images and return predictions.
#     """
#     user_id = request.user.idusers
#     user_name = request.user.username
#     pallets_count = 0
#     detect_rest = None
#     insert_time = datetime.now()
#     folder_name = f'static/{user_name}'
#     image_paths = []
#
#     try:
#         for img_file in files:
#             contents = await img_file.read()
#             input_img = Image.open(BytesIO(contents))
#             pallets_count, full_img_path = img_pred(input_img, folder_name, img_file.filename)
#             image_paths.append(full_img_path)
#
#             # Calculate additional data
#             price_piece = 41
#             tranport_fc = 0.015
#             co2_fc = 34.77
#             transport_cost = 700
#             transport_fc_count = pallets_count * 0.015 if buy_or_sell == "buy" else 0
#             total_transport = transport_fc_count * 700 if buy_or_sell == "buy" else 0
#             total_price = pallets_count * price_piece
#             #transport_fc_count = pallets_count * tranport_fc
#             co2_saving_count = transport_fc_count * co2_fc
#             #total_transport = transport_fc_count * transport_cost
#
#             success = await insert_img(db, full_img_path, user_id, pallets_count, insert_time, price_piece, tranport_fc, co2_fc, transport_cost, total_price, transport_fc_count, co2_saving_count, total_transport)
#
#             if not success:
#                 raise HTTPException(status_code=500, detail="Failed to insert data into database")
#
#
#         # Send email with images and pallets count
#         subject = "Pallets Count Report"
#         message = "Attached are the images uploaded and their corresponding pallets count."
#         send_email_with_images_and_count(email_to, subject, message, image_paths, pallets_count)
#
#         # Return JSON response with calculated data
#         return JSONResponse(status_code=status.HTTP_200_OK, content={
#             "message": "Images uploaded and email sent successfully.",
#             "pallets_count": pallets_count,
#             "Price_piece": price_piece,
#             "total_price": total_price,
#             "transport_fc_count": transport_fc_count,
#             "Co2_saving_count": co2_saving_count,
#             "total_transport": total_transport,
#             "Price_piece": price_piece,
#             "co2_fc": co2_fc,
#             "transport_cost": transport_cost,
#             "buy_or_sell": buy_or_sell
#
#         })
#
#     except Exception as e:
#         # Log the error
#         print(f"Error during image upload: {e}")
#         # Return an error response
#
#         msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
#         logger.error(f'From {request.endpoint} {msg}', exc_info=e)
#         # return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
#         #     "message": "An error occurred during image upload."})

# @router.post("/image_upload", summary="Get pallets count")
# async def upload_img(request: Request,
#                      files: list[UploadFile],  # Non-default argument
#                      user: User = Depends(oauth2_scheme),
#                      db: Session = Depends(get_db)
#                      ):
#     """
#     Upload images and return predictions.
#     """
#     user_id = request.user.idusers
#     user_name = request.user.username
#     pallets_count = 0
#     detect_rest = None
#     insert_time = datetime.now()
#     folder_name = f'/home/cyber-makarov/pallet_fast/static/{user_name}'
#
#     try:
#         for img_file in files:
#             contents = await img_file.read()
#             input_img = Image.open(BytesIO(contents))
#             pallets_count, detect_rest, full_img_path = img_pred(input_img, folder_name, img_file.filename)
#
#             success = await insert_img(db, full_img_path, user_id, pallets_count, insert_time)
#
#             if not success:
#                 raise HTTPException(status_code=500, detail="Failed to insert data into database")
#
#     except Exception as e:
#         # Log the error
#         print(f"Error during image upload: {e}")
#         # Return an error response
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             content={"message": "An error occurred during image upload."})
