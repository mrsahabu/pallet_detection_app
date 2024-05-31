from typing import List
from aiosmtplib import status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from core.database import get_db
from fastapi import Depends
from venv import logger
from fastapi import APIRouter, Request, UploadFile
from .utils import image_prediction
from .services import insert_data
from fastapi import APIRouter
from io import BytesIO
import sys
from datetime import datetime
from fastapi import HTTPException, status
from core.security import oauth2_scheme
from user.models import UserModel
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from io import BytesIO
from typing import List
from core.database import get_db
from user.models import UserModel, DataModel
from .response import DataModelResponse
import sys
from PIL import Image

User = UserModel()

router = APIRouter(
    prefix="/pallet_detection",
    tags=["pallet detection system"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/upload", summary="Upload images and return predictions")
async def upload_images(
    request: Request,
    files: List[UploadFile] = File(...),
    buy_or_sell: str = Form(...),
    user: UserModel = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        user_id = request.user.id
        user_name = request.user.username
        pallets_count = 0
        insert_time = datetime.now()
        folder_name = f'static/{user_name}'
        image_paths = []

        for img_file in files:
            contents = await img_file.read()
            input_img = Image.open(BytesIO(contents))
            pallets_count, full_img_path = image_prediction(input_img, folder_name, img_file.filename)
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
        success = await insert_data(
            db,
            image_paths,
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


@router.get('/users/data',  response_model=List[DataModelResponse], status_code=status.HTTP_200_OK)
async def get_data_with_files(
    request: Request,
    user: UserModel = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    if request.user.role == "admin":
        base_url = str(request.base_url).rstrip("/")
        # Query all data from DataModel
        user_data = db.query(DataModel).all()
        result = []
        for data in user_data:
            item = {
                "data_id": data.id,
                "user_id": data.user_id,
                "pallets_count": data.pallets_count,
                "insert_time": data.insert_time,
                "price_piece": data.price_piece,
                "total_price": data.total_price,
                "transport_fc_count": data.transport_fc_count,
                "co2_saving_count": data.co2_saving_count,
                "total_transport": data.total_transport,
                "co2_fc": data.co2_fc,
                "transport_cost": data.transport_cost,
                "buy_or_sell": data.buy_or_sell,
                "files": [{"id": file.id, "img_path": f"{base_url}/images/{'/'.join(file.img_path.split('/')[1:])}"} for file in data.files]
            }
            result.append(item)

        return result
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
            "message": "Unauthorized access"
        })
        
@router.get('/user/data',  response_model=List[DataModelResponse], status_code=status.HTTP_200_OK)
async def get_data_with_files(
    request: Request,
    user: UserModel = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    base_url = str(request.base_url).rstrip("/")
    # Query all data from DataModel
    user_data = db.query(DataModel).filter_by(user_id=request.user.id).all()
    result = []
    for data in user_data:
        item = {
            "data_id": data.id,
            "user_id": data.user_id,
            "pallets_count": data.pallets_count,
            "insert_time": data.insert_time,
            "price_piece": data.price_piece,
            "total_price": data.total_price,
            "transport_fc_count": data.transport_fc_count,
            "co2_saving_count": data.co2_saving_count,
            "total_transport": data.total_transport,
            "co2_fc": data.co2_fc,
            "transport_cost": data.transport_cost,
            "buy_or_sell": data.buy_or_sell,
            "files": [{"id": file.id, "img_path": f"{base_url}/images/{'/'.join(file.img_path.split('/')[1:])}"} for file in data.files]
        }
        result.append(item)

    return result