from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from user.models import DataModel, FileModel


async def insert_data(
    db: Session,
    img_paths: List[str],
    user_id: int,
    pallets_count: int,
    insert_time: datetime,
    price_piece: float,
    total_price: float,
    transport_fc_count: float,
    co2_saving_count: float,
    total_transport: float,
    co2_fc: float,
    transport_cost: float,
    buy_or_sell: str
):
    try:
        data = DataModel(
            user_id=user_id,
            pallets_count=pallets_count,
            insert_time=insert_time,
            price_piece=price_piece,
            total_price=total_price,
            transport_fc_count=transport_fc_count,
            co2_saving_count=co2_saving_count,
            total_transport=total_transport,
            co2_fc=co2_fc,
            transport_cost=transport_cost,
            buy_or_sell=buy_or_sell
        )
        db.add(data)
        db.commit()
        db.refresh(data)

        for img_path in img_paths:
            await insert_file(db, data.id, img_path)
    except Exception as e:
        raise e
        return False
    return True


async def insert_file(
    db: Session,
    data_id: int,
    file_path: str
):
    try:
        file_data = FileModel(data_id=data_id, img_path=file_path)
        db.add(file_data)
        db.commit()
        db.refresh(file_data)
   
    except Exception as e:
        raise e
    
def get_all_users_data(db: Session):
    user_data = db.query(DataModel).all()
    images_data = db.query(FileModel).all()
    return user_data